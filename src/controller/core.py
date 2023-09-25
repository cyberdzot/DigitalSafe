from controller.consts import Const
from global_consts.g_consts import GConst
from ui.console.utils import Console
from ui.console.windows import Windows
from os import path, mkdir  # позже импортацию конкретезировать
from db.data_base_sqlite import SQLite


class Core():
    """Ядро программы(Контроллер)."""

    def start_program(self):
        """Запуск программы."""
        #
        self.db_init()
        self.ui_init()

    def db_init(self):
        """Инициализация базы данных на старте программы."""
        #
        data_dir = path.dirname(path.realpath(__file__)) + '\\data'
        if not path.isdir(data_dir):
            mkdir(data_dir)
        self.__sql_connect = SQLite(data_dir + '\\test.sqlite', False)
        # создать таблицу если её нету:
        SQLite.exec_query(self.__sql_connect, Const.Q_NEW_TABLE.value)

    def ui_init(self):
        """Запуск всего UI в консоли."""
        #
        self.__windows = Windows()
        #
        while True:
            Console.clear()
            # отрисуем консоль
            match self.__windows.get_window():
                case GConst.WIN_MANUAL.value:
                    self.__windows.window_manual()
                case GConst.WIN_AUTH.value:
                    self.__windows.window_auth()
                case GConst.WIN_REG.value:
                    self.__windows.window_reg()
                case GConst.WIN_LOGIN.value:
                    self.__windows.window_login()
                case GConst.WIN_EXIT.value:
                    break
                # case _:
                #     pass
            # отработаем по запросам к БД, если таковы имеются
            query = self.__windows.get_query()
            match query[0]:
                # регистрация аккаунта в сейфе, успешно ли зарегало? или уже есть такой акк?
                case GConst.QUERY_REG.value:
                    result = SQLite.exec_read_query(
                        self.__sql_connect, 'SELECT name FROM users WHERE name = ?;', (query[1],))
                    if result == []:
                        SQLite.exec_query(
                            self.__sql_connect, 'INSERT INTO users (name, pass) VALUES (?, ?);', query[1:])
                        self.__windows.set_window(
                            GConst.WIN_AUTH.value, 'Аккаунт с именем ' + query[1] +
                            ' успешно зарегистрирован в базе.')
                    else:
                        self.__windows.set_window(
                            GConst.WIN_AUTH.value, 'Аккаунт с именем ' + query[1] +
                            ' уже зарегистрирован в базе, придумайте себе другое имя!')
            # обнуляем запрос
            self.__windows.add_query((None, None, None))
            # вход в систему, существует ли такой акк и пароль?
            # достать все ресурсы на аккаунте
            # добавить ресурс в аккаунт
            # удалить ресурс из аккаунта
