"""Модуль, отвечающий за отрисовку данных в консоли."""

from pyperclip import copy as copy_in_buffer
from entities.hash import get_hash
from global_consts.g_consts import GConst
from ui.console.consts import Const
from ui.console.utils import Console
from entities.account_data import AccountData
from entities.scrambler import Cipher


class Windows:
    """Окна для консоли."""

    def __init__(self, console: Console, name_and_version: tuple):
        self.__app_name = name_and_version[0]
        self.__app_version = name_and_version[1]
        self.__console = console
        self.__account = None
        self.__cipher = None
        self.__view_resource = None
        self.__open_window = GConst.WIN_MANUAL.value
        self.__query = Const.QUERY_NULL.value
        self.__warn = ""
        self.__ans1 = ""
        self.__ans2 = ""
        self.__ans3 = ""
        self.__winstr = []

    def sync_account(self, account: AccountData, cipher: Cipher):
        """Начальная синхронизация аккаунта для связки UI с Core."""
        self.__account = account
        self.__cipher = cipher

    def set_window(self, window: int, warn=""):
        """Показать выбранное окно."""
        self.__open_window = window
        self.__warn = warn

    def get_window(self) -> int:
        """Узнать текущее отображаемое окно."""
        return self.__open_window

    # ---------------------------------------------------

    def update_window(self):
        """Обновить показ окна(прежде наполняется инфой из переменных)."""
        self.__console.message(
            "============== "
            + self.__app_name
            + " ver. "
            + self.__app_version
            + " =============="
        )
        self.__console.message("                     (╯-_-)╯")
        self.__console.warn(self.__warn + "\n")

        # переберём строки к показу
        for string in self.__winstr:
            self.__console.message(string)

    def add_query(self, data_for_query: tuple):
        """Добавить кортёж с данными для запроса к БД."""
        self.__query = data_for_query

    def get_query(self) -> tuple:
        """Узнать запрос к БД(если такой имеется) из интерфейса."""
        temp = self.__query
        # отправка и очистка запроса, чтобы не зацикливало в core
        self.__query = Const.QUERY_NULL.value
        return temp  # ('id query', 'arg1', 'arg2', 'arg3')

    # ---------------------------------------------------

    def window_manual(self):
        """Окно - (1). Знакомство с программой, инструкция."""
        #
        self.__winstr = [
            "Приветствую тебя пользователь,",
            'в программе для хранения данных(в формате "Ресурс-Логин-Пароль").',
            "На любой стадии исполнения программы отправьте пустой ввод,",
            "чтобы вернуться на предыдущее окно в консоли,",
            "на данном этапе это закрытие программы.",
        ]
        self.update_window()
        #
        self.__ans1 = input(
            "\nВведите любую цифру(или символ) и нажмите ввод, чтобы продолжить..."
        )
        if self.__ans1 == "":
            self.set_window(GConst.WIN_EXIT.value)
            return
        self.set_window(GConst.WIN_AUTHENTICATION.value)

    def window_authentication(self):
        """Окно - (2). Авторизация(выбор - вход или регистрация)."""
        #
        self.__winstr = [
            "Вы хотите войти[1] или зарегистрироваться[2]?",
        ]
        self.update_window()
        #
        self.__ans1 = input("\nВведите цифру: ")
        if self.__ans1 == "":
            self.set_window(GConst.WIN_MANUAL.value)
            return
        #
        if self.__ans1 == "1":
            self.set_window(GConst.WIN_LOGIN.value)
        elif self.__ans1 == "2":
            self.set_window(GConst.WIN_REGISTRATION.value)
        else:
            self.set_window(
                GConst.WIN_AUTHENTICATION.value,
                "Введите одну из двух цифр(1 или 2), как указано выше.",
            )

    def window_registration(self):
        """Окно - (2.1). Регистрация."""
        #
        self.__winstr = [
            "Для регистрации нужно ввести логин и пароль по очереди.",
        ]
        self.update_window()
        #
        self.__ans1 = input("Введите логин: ")
        if self.__ans1 == "":
            self.set_window(GConst.WIN_AUTHENTICATION.value)
            return
        self.__ans2 = input("Введите пароль: ")
        if self.__ans2 == "":
            self.set_window(GConst.WIN_AUTHENTICATION.value)
            return
        self.__ans2 = get_hash(self.__ans2)
        self.add_query((GConst.QUERY_REGISTRATION.value,
                       self.__ans1, self.__ans2))

    def window_login(self):
        """Окно - (3). Вход."""
        #
        self.__winstr = [
            "Для входа нужно ввести логин и пароль по очереди.",
        ]
        self.update_window()
        #
        self.__ans1 = input("Введите логин: ")
        if self.__ans1 == "":
            self.set_window(GConst.WIN_AUTHENTICATION.value)
            return
        self.__ans2 = input("Введите пароль: ")
        if self.__ans2 == "":
            self.set_window(GConst.WIN_AUTHENTICATION.value)
            return
        self.__ans2 = get_hash(self.__ans2)
        self.add_query((GConst.QUERY_LOGIN.value, self.__ans1, self.__ans2))

    def resources_append(self):
        """Добавить имеющиеся ресурсы в список главного меню."""
        for row in self.__account.get_user_data():
            concat = "[" + str(row[0]) + "]"
            for col in row[1:3]:
                concat = concat + " " + str(col)
            concat = concat + " ******"
            self.__winstr.append(concat)
        self.__winstr.append("")

    def window_main_menu(self):
        """Окно - (4). Главное меню."""
        self.__winstr = [
            "[0] ...Добавить новый...",
            "Ваши ресурсы:",
        ]
        self.resources_append()
        self.update_window()
        #
        self.__ans1 = input("Введите цифру: ")
        if self.__ans1 == "":
            # если пустой ввод - разлогиниваемся
            self.set_window(GConst.WIN_AUTHENTICATION.value)
            return
        elif self.__ans1 == "0":
            # добавляем ресурс
            self.set_window(GConst.WIN_ADD_RESOURCE.value)
            return

        # запоминаем выбранный ресурс из списка
        for row in self.__account.get_user_data():
            # 0-id 1-resname 2-login 3-pass
            # concat = f'{row[0]} {row[1]} {row[2]} {row[3]}'
            # concat = " ".join(row)
            ans1_int = int(self.__ans1)
            if ans1_int == row[0]:
                self.__view_resource = row
                self.set_window(GConst.WIN_VIEW_RESOURCE.value)
                return
            if ans1_int < row[0]:
                break
        self.set_window(
            GConst.WIN_MAIN_MENU.value, "Недопустимый выбор! Попробуйте ещё раз."
        )

    def window_add_resource(self):
        """Окно - (5). Добавление нового ресурса."""
        self.__winstr = [
            "Введите данные ресурса по очереди.",
            "",
        ]
        self.update_window()
        #
        self.__ans1 = input("Введите название: ")
        if self.__ans1 == "":
            self.set_window(GConst.WIN_MAIN_MENU.value)
            return
        self.__ans2 = input("Введите логин: ")
        if self.__ans2 == "":
            self.set_window(GConst.WIN_MAIN_MENU.value)
            return
        self.__ans3 = input("Введите пароль: ")
        if self.__ans3 == "":
            self.set_window(GConst.WIN_MAIN_MENU.value)
            return
        # шифруем пароль
        self.__ans3 = self.__cipher.aes_cbc_pbkdf2_encrypt_to_base64(
            self.__ans3)
        # добавим новый в переменную и в БД по очереди
        self.add_query(
            (GConst.QUERY_ADD_RESOURCE.value, self.__ans1, self.__ans2, self.__ans3)
        )
        self.set_window(
            GConst.WIN_MAIN_MENU.value, "Данные к новому ресурсу добавлены."
        )

    def window_view_resource(self):
        """Окно - (6). Просмотр ресурса."""
        self.__winstr = [
            "Вы можете выбрать выбрать цифру от 1 до 3, чтобы скопировать данные в буфер обмена",
            "[0] ...Стереть эти данные...",
            "Данные:",
            # тут будет выводить ID ресурса, чтобы можно было менять ID
        ]
        decrypt_data = self.__cipher.aes_cbc_pbkdf2_decrypt_from_base64(
            self.__view_resource[3]
        )
        self.__winstr.append("[1] Ресурс:\t" + (self.__view_resource[1]))
        self.__winstr.append("[2] Логин:\t" + self.__view_resource[2])
        self.__winstr.append("[3] Пароль:\t" + decrypt_data)

        self.update_window()
        #
        self.__ans1 = input("Введите цифру: ")
        match self.__ans1:
            case "":
                # возвращаемся назад
                self.set_window(GConst.WIN_MAIN_MENU.value)
            case "0":
                # удаляем ресурс по значению,
                # то бишь список со значениями (self.__view_resource)
                # и возвращаемся назад
                self.add_query(
                    (GConst.QUERY_DEL_RESOURCE.value, self.__view_resource))
                self.set_window(GConst.WIN_MAIN_MENU.value)
            case "1" | "2":
                copy_in_buffer(self.__view_resource[int(self.__ans1)])
                self.set_window(
                    GConst.WIN_VIEW_RESOURCE.value,
                    "Выбранные данные успешно скопированы в буфер обмена.",
                )
            case "3":
                copy_in_buffer(decrypt_data)
                self.set_window(
                    GConst.WIN_VIEW_RESOURCE.value,
                    "Выбранные данные успешно скопированы в буфер обмена.",
                )
            case _:
                self.set_window(
                    GConst.WIN_VIEW_RESOURCE.value,
                    "Недопустимый выбор! Попробуйте ещё раз.",
                )
