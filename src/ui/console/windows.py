from global_consts.g_consts import GConst
from ui.console.consts import Const
from ui.console.utils import Console


class Windows():
    """Окна для консоли."""

    __open_window = GConst.WIN_MANUAL.value
    __warn = ''
    __ans1 = ''
    __ans2 = ''
    __winstr = []
    __query = (None, None, None)
    # ---------------------------------------------------

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
        Console.message('============== ' + Const.PROG_NAME.value + ' ver. '
                        + Const.PROG_VERSION.value + ' ==============\n')
        Console.warn(self.__warn + '\n')

        # переберём строки к показу
        for str in self.__winstr:
            Console.message(str)

    def add_query(self, data_for_query: tuple):
        self.__query = data_for_query

    def get_query(self) -> tuple:
        """Узнать запрос к БД(если такой имеется) из интерфейса."""
        return self.__query  # ('id query', 'arg1', 'arg2...')
    # ---------------------------------------------------

    def window_manual(self):
        """Окно - (X). Ожидание."""
        pass

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
        self.set_window(GConst.WIN_AUTH.value)

    def window_auth(self):
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
            self.set_window(GConst.WIN_REG.value)
        else:
            self.__warn = 'Введите одну из двух цифр(1 или 2), как указано выше.'

    def window_reg(self):
        """Окно - (2.1). Регистрация."""
        #
        self.__winstr = [
            'Для регистрации нужно ввести логин и пароль по очереди.',
        ]
        self.update_window()
        #
        self.__ans1 = input('Введите логин: ')
        self.__ans2 = input('Введите пароль: ')
        if self.__ans1 == "" or self.__ans2 == "":
            self.set_window(GConst.WIN_AUTH.value)
            return
        self.add_query((GConst.QUERY_REG.value, self.__ans1, self.__ans2))

    def window_login(self):
        """Окно - (3). Вход."""
        #
        self.__winstr = [
            'Для входа нужно ввести логин и пароль по очереди.',
        ]
        self.update_window()

        self.__ans1 = input('Введите логин: ')
        if self.__ans1 == "":
            self.set_window(GConst.WIN_AUTH.value)
            return
        self.__ans2 = input('Введите пароль: ')
        if self.__ans2 == "":
            self.set_window(GConst.WIN_AUTH.value)
            return
        self.set_window(GConst.WIN_LOGIN.value)
        # todo: здесь будем отправлять в контроллёр данные которые он перенаправит в БД и результат вернёт сюда
