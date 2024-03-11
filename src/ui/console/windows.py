"""Модуль, отвечающий за отрисовку данных в консоли."""

from pyperclip import copy as copy_in_buffer
from utils.utils_others import get_hash  # pylint:disable=E0401
from utils.utils_consts import ConstAutoNum, ConstUI  # pylint:disable=E0401
from utils.utils_console import Console  # pylint:disable=E0401
from entities.account_data import AccountData  # pylint:disable=E0401
from entities.scrambler import Cipher  # pylint:disable=E0401


class ConsoleUI:
    """Виртуальные окна в консоли."""

    def __init__(self, console: Console, app_info: tuple, cipher: Cipher):
        self.__open_window = ConstAutoNum.WIN_MANUAL.value
        self.__query = ConstUI.QUERY_NULL.value
        self.__app_info = app_info
        self.__console = console
        self.__account = None
        self.__cipher = cipher
        self.__view_resource = None
        self.__warn = ""
        self.__ans = ["", "", ""]
        self.__messages = []

    def sync_account(self, account: AccountData):
        """Начальная синхронизация аккаунта для связки UI с Core."""
        self.__account = account

    def set_window(self, window: int, warn=""):
        """Выбрать ID окна для отображения и возможность показать предупреждение в нём."""
        self.__open_window = window
        self.__warn = warn

    def get_window(self) -> int:
        """Получить ID текущего отображаемого окна."""
        return self.__open_window

    def update_window(self):
        """Обновить показ окна(прежде наполняется инфой из переменных)."""
        self.__console.message(
            "============== "
            + self.__app_info[0]
            + " ver. "
            + self.__app_info[1]
            + " =============="
        )
        self.__console.message("                     (╯-_-)╯")
        self.__console.warn(self.__warn + "\n")

        # переберём строки к показу
        for string in self.__messages:
            self.__console.message(string)

    # ---------------------------------------------------

    def add_query(self, data: tuple):
        """Добавить кортёж с данными для запроса к БД."""
        self.__query = data

    def get_query(self) -> tuple:
        """Узнать запрос к БД(если такой имеется) из интерфейса."""
        temp = self.__query
        # отправка и очистка запроса, чтобы не зацикливало в core
        self.__query = ConstUI.QUERY_NULL.value
        return temp  # ('id query', 'arg1', 'arg2', 'arg3')

    # ---------------------------------------------------

    def window_manual(self):
        """Окно - (1). Знакомство с программой, инструкция."""
        #
        self.__messages = [
            "Приветствую тебя пользователь,",
            'в программе для хранения данных(в формате "Ресурс-Логин-Пароль").',
            "На любой стадии исполнения программы отправьте пустой ввод",
            "для возврата на предыдущее окно в консоли,",
            "на данном этапе это закрытие программы.",
        ]
        self.update_window()
        #
        self.__ans[0] = input(
            "\nВведите любую цифру(или символ) и нажмите ввод, чтобы продолжить..."
        )
        if self.__ans[0] == "":
            self.set_window(ConstAutoNum.WIN_EXIT.value)
            return
        self.set_window(ConstAutoNum.WIN_AUTHENTICATION.value)

    def window_authentication(self):
        """Окно - (2). Авторизация(выбор - вход или регистрация)."""
        #
        self.__messages = [
            "Вы хотите войти[1] или зарегистрироваться[2]?",
        ]
        self.update_window()
        #
        self.__ans[0] = input("\nВведите цифру: ")
        if self.__ans[0] == "":
            self.set_window(ConstAutoNum.WIN_MANUAL.value)
            return
        #
        if self.__ans[0] == "1":
            self.set_window(ConstAutoNum.WIN_LOGIN.value)
        elif self.__ans[0] == "2":
            self.set_window(ConstAutoNum.WIN_REGISTRATION.value)
        else:
            self.set_window(
                ConstAutoNum.WIN_AUTHENTICATION.value,
                "Введите одну из двух цифр(1 или 2), как указано выше.",
            )

    def window_registration(self):
        """Окно - (2.1). Регистрация."""
        #
        self.__messages = [
            "Для регистрации нужно ввести логин и пароль по очереди.",
        ]
        self.update_window()
        #
        self.__ans[0] = input("Введите логин: ")
        if self.__ans[0] == "":
            self.set_window(ConstAutoNum.WIN_AUTHENTICATION.value)
            return
        self.__ans[1] = input("Введите пароль: ")
        if self.__ans[1] == "":
            self.set_window(ConstAutoNum.WIN_AUTHENTICATION.value)
            return
        self.__ans[1] = get_hash(self.__ans[1])
        self.add_query((ConstAutoNum.QUERY_REGISTRATION.value,
                       self.__ans[0], self.__ans[1]))

    def window_login(self):
        """Окно - (3). Вход."""
        #
        self.__messages = [
            "Для входа нужно ввести логин и пароль по очереди.",
        ]
        self.update_window()
        #
        self.__ans[0] = input("Введите логин: ")
        if self.__ans[0] == "":
            self.set_window(ConstAutoNum.WIN_AUTHENTICATION.value)
            return
        self.__ans[1] = input("Введите пароль: ")
        if self.__ans[1] == "":
            self.set_window(ConstAutoNum.WIN_AUTHENTICATION.value)
            return
        self.__ans[1] = get_hash(self.__ans[1])
        self.add_query((ConstAutoNum.QUERY_LOGIN.value,
                       self.__ans[0], self.__ans[1]))

    def resources_append(self):
        """Добавить имеющиеся ресурсы в список главного меню."""
        #
        for row in self.__account.get_user_data():
            concat = "[" + str(row[0]) + "]"
            for col in row[1:3]:
                concat = concat + " " + str(col)
            concat = concat + " ******"
            self.__messages.append(concat)
        self.__messages.append("")

    def window_main_menu(self):
        """Окно - (4). Главное меню."""
        #
        self.__messages = [
            "[0] ...Добавить новый...",
            "Ваши ресурсы:",
        ]
        self.resources_append()
        self.update_window()
        #
        self.__ans[0] = input("Введите цифру: ")
        if self.__ans[0] == "":
            # если пустой ввод - разлогиниваемся
            self.set_window(ConstAutoNum.WIN_AUTHENTICATION.value)
            return
        elif self.__ans[0] == "0":
            # добавляем ресурс
            self.set_window(ConstAutoNum.WIN_ADD_RESOURCE.value)
            return

        # запоминаем выбранный ресурс из списка
        for row in self.__account.get_user_data():
            # 0-id 1-resname 2-login 3-pass
            # concat = f'{row[0]} {row[1]} {row[2]} {row[3]}'
            # concat = " ".join(row)
            ans1_int = int(self.__ans[0])
            if ans1_int == row[0]:
                self.__view_resource = row
                self.set_window(ConstAutoNum.WIN_VIEW_RESOURCE.value)
                return
            if ans1_int < row[0]:
                break
        self.set_window(
            ConstAutoNum.WIN_MAIN_MENU.value, "Недопустимый выбор! Попробуйте ещё раз."
        )

    def window_add_resource(self):
        """Окно - (5). Добавление нового ресурса."""
        #
        self.__messages = [
            "Введите данные ресурса по очереди.",
            "",
        ]
        self.update_window()
        #
        self.__ans[0] = input("Введите название: ")
        if self.__ans[0] == "":
            self.set_window(ConstAutoNum.WIN_MAIN_MENU.value)
            return
        self.__ans[1] = input("Введите логин: ")
        if self.__ans[1] == "":
            self.set_window(ConstAutoNum.WIN_MAIN_MENU.value)
            return
        self.__ans[2] = input("Введите пароль: ")
        if self.__ans[2] == "":
            self.set_window(ConstAutoNum.WIN_MAIN_MENU.value)
            return
        # шифруем пароль
        self.__ans[2] = self.__cipher.aes_cbc_pbkdf2_encrypt_to_base64(
            self.__ans[2])
        # добавим новый в переменную и в БД по очереди
        self.add_query(
            (ConstAutoNum.QUERY_ADD_RESOURCE.value,
             self.__ans[0], self.__ans[1], self.__ans[2])
        )
        self.set_window(
            ConstAutoNum.WIN_MAIN_MENU.value, "Данные к новому ресурсу добавлены."
        )

    def window_view_resource(self):
        """Окно - (6). Просмотр ресурса."""
        #
        self.__messages = [
            "Вы можете выбрать выбрать цифру от 1 до 3, чтобы скопировать данные в буфер обмена",
            "[0] ...Стереть эти данные...",
            "Данные:",
            # тут будет выводить ID ресурса, чтобы можно было менять ID
        ]
        decrypt_data = self.__cipher.aes_cbc_pbkdf2_decrypt_from_base64(
            self.__view_resource[3]
        )
        self.__messages.append("[1] Ресурс:\t" + (self.__view_resource[1]))
        self.__messages.append("[2] Логин:\t" + self.__view_resource[2])
        self.__messages.append("[3] Пароль:\t" + decrypt_data)

        self.update_window()
        #
        self.__ans[0] = input("Введите цифру: ")
        match self.__ans[0]:
            case "":
                # возвращаемся назад
                self.set_window(ConstAutoNum.WIN_MAIN_MENU.value)
            case "0":
                # удаляем ресурс по значению, и возвращаемся назад
                self.add_query(
                    (ConstAutoNum.QUERY_DEL_RESOURCE.value, self.__view_resource))
                self.set_window(ConstAutoNum.WIN_MAIN_MENU.value)
            case "1" | "2":
                copy_in_buffer(self.__view_resource[int(self.__ans[0])])
                self.set_window(
                    ConstAutoNum.WIN_VIEW_RESOURCE.value,
                    "Выбранные данные успешно скопированы в буфер обмена.",
                )
            case "3":
                copy_in_buffer(decrypt_data)
                self.set_window(
                    ConstAutoNum.WIN_VIEW_RESOURCE.value,
                    "Выбранные данные успешно скопированы в буфер обмена.",
                )
            case _:
                self.set_window(
                    ConstAutoNum.WIN_VIEW_RESOURCE.value,
                    "Недопустимый выбор! Попробуйте ещё раз.",
                )
