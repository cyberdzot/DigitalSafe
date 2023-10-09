from global_consts.g_consts import GConst
from ui.console.consts import Const
from ui.console.utils import Console
from entities.account_data import AccountData


class Windows():
    """Окна для консоли."""

    __open_window = GConst.WIN_MANUAL.value
    __warn = ''
    __ans1 = ''
    __ans2 = ''
    __ans3 = ''
    __winstr = []
    __query = Const.QUERY_NULL.value
    # ---------------------------------------------------
    
    def __init__(self, name_and_version: tuple):
        self.app_name = name_and_version[0]
        self.app_version = name_and_version[1]


    def sync_account(self, account: AccountData):
        """Связать модуль консоли(Окна) с аккаунтом, для синхронизации между окнами и контроллером."""
        self.__account = account

    def set_window(self, window: int, warn=''):
        """Показать выбранное окно."""
        self.__open_window = window
        self.__warn = warn

    def get_window(self) -> int:
        """Узнать текущее отображаемое окно."""
        return self.__open_window
    # ---------------------------------------------------

    def update_window(self):
        """Обновить показ окна(прежде наполняется инфой из переменных)."""
        Console.message('============== ' + self.app_name + ' ver. '
                        + self.app_version + ' ==============\n')
        Console.warn(self.__warn + '\n')

        # переберём строки к показу
        for str in self.__winstr:
            Console.message(str)

    def add_query(self, data_for_query: tuple):
        """Добавить кортёж с данными для запроса к БД."""
        self.__query = data_for_query

    def get_query(self) -> tuple:
        """Узнать запрос к БД(если такой имеется) из интерфейса."""
        temp = self.__query
        # отправим данные для запроса и очистим __query, только наоборот =]
        self.__query = Const.QUERY_NULL.value
        return temp  # ('id query', 'arg1', 'arg2', 'arg3')
    # ---------------------------------------------------

    # def window_wait(self):
    #     """Окно - (X). Ожидание."""
    #     pass

    def window_manual(self):
        """Окно - (1). Знакомство с программой, инструкция."""
        #
        self.__winstr = [
            'Приветствую тебя пользователь,',
            'в программе для хранения данных(в формате "Ресурс-Логин-Пароль").',
            'На любой стадии исполнения программы отправьте пустой ввод,',
            'чтобы вернуться на предыдущее окно в консоли,',
            'на данном этапе это закрытие программы.'
        ]
        self.update_window()
        #
        self.__ans1 = input(
            '\nВведите любую цифру(или символ) и нажмите ввод, чтобы продолжить...')
        if self.__ans1 == "":
            self.set_window(GConst.WIN_EXIT.value)
            return
        self.set_window(GConst.WIN_AUTHENTICATION.value)

    def window_authentication(self):
        """Окно - (2). Авторизация(выбор - вход или регистрация)."""
        #
        self.__winstr = [
            'Вы хотите войти[1] или зарегистрироваться[2]?',
        ]
        self.update_window()
        #
        self.__ans1 = input('\nВведите цифру: ')
        if self.__ans1 == "":
            self.set_window(GConst.WIN_MANUAL.value)
            return
        #
        if self.__ans1 == '1':
            self.set_window(GConst.WIN_LOGIN.value)
        elif self.__ans1 == '2':
            self.set_window(GConst.WIN_REGISTRATION.value)
        else:
            self.set_window(GConst.WIN_AUTHENTICATION.value,
                            'Введите одну из двух цифр(1 или 2), как указано выше.')

    def window_registration(self):
        """Окно - (2.1). Регистрация."""
        #
        self.__winstr = [
            'Для регистрации нужно ввести логин и пароль по очереди.',
        ]
        self.update_window()
        #
        self.__ans1 = input('Введите логин: ')
        if self.__ans1 == "":
            self.set_window(GConst.WIN_AUTHENTICATION.value)
            return
        self.__ans2 = input('Введите пароль: ')
        if self.__ans2 == "":
            self.set_window(GConst.WIN_AUTHENTICATION.value)
            return
        self.add_query((GConst.QUERY_REGISTRATION.value,
                       self.__ans1, self.__ans2))

    def window_login(self):
        """Окно - (3). Вход."""
        #
        self.__winstr = [
            'Для входа нужно ввести логин и пароль по очереди.',
        ]
        self.update_window()
        #
        self.__ans1 = input('Введите логин: ')
        if self.__ans1 == "":
            self.set_window(GConst.WIN_AUTHENTICATION.value)
            return
        self.__ans2 = input('Введите пароль: ')
        if self.__ans2 == "":
            self.set_window(GConst.WIN_AUTHENTICATION.value)
            return
        self.add_query((GConst.QUERY_LOGIN.value, self.__ans1, self.__ans2))

    def resources_append(self):
        """Добавить имеющиеся ресурсы в список главного меню."""
        for row in self.__account.get_user_data():
            concat = '[' + str(row[0]) + ']'
            for col in row[1:]:
                concat = concat + ' ' + str(col)
            self.__winstr.append(concat)
        self.__winstr.append('')

    def window_main_menu(self):
        """Окно - (4). Главное меню."""
        self.__winstr = [
            '[0] Добавить новый...(╯-_-)╯',
            'Ваши ресурсы:',
        ]
        self.resources_append()
        self.update_window()
        #
        self.__ans1 = input('Введите цифру: ')
        if self.__ans1 == "":
            self.set_window(GConst.WIN_AUTHENTICATION.value)
            # разлогинивается тут
            return
        if self.__ans1 == "0":
            self.set_window(GConst.WIN_ADD_RESOURCE.value)
            return
        # ? здесь выбираем добавление нового рес-а или просмотр имеющихся
        self.set_window(GConst.WIN_MAIN_MENU.value, 'Недопустимый выбор! Попробуйте ещё раз.')

    def window_add_resource(self):
        """Окно - (5). Добавление нового ресурса."""
        self.__winstr = [
            'Введите данные ресурса по очереди.',
            '',
        ]
        self.update_window()
        #
        self.__ans1 = input('Введите название: ')
        if self.__ans1 == "":
            self.set_window(GConst.WIN_MAIN_MENU.value)
            return
        self.__ans2 = input('Введите логин: ')
        if self.__ans2 == "":
            self.set_window(GConst.WIN_MAIN_MENU.value)
            return
        self.__ans3 = input('Введите пароль: ')
        if self.__ans3 == "":
            self.set_window(GConst.WIN_MAIN_MENU.value)
            return
        # добавим новый в переменную и в БД по очереди
        self.add_query((GConst.QUERY_ADD_RESOURCE.value,
                       self.__ans1, self.__ans2, self.__ans3))
        self.set_window(GConst.WIN_MAIN_MENU.value,
                        'Данные к новому ресурсу добавлены.')

    def window_view_resource(self):
        pass
