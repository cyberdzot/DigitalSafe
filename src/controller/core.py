from controller.consts import Const
from global_consts.g_consts import GConst
from ui.console.utils import Console
from ui.console.windows import Windows
from os import path, mkdir  # todo позже импортацию конкретезировать
from db.data_base_sqlite import SQLite
from entities.account_data import AccountData


class Core:
    """Ядро программы (Контроллер)."""

    def run_application(self, name_and_version: tuple):
        """Запуск ядра программы."""
        #
        self.db_init()
        self.ui_init(name_and_version)

    def db_init(self):
        """Инициализация базы данных на старте программы."""
        #
        data_dir = path.dirname(path.realpath(__file__)) + '\\data'
        if not path.isdir(data_dir):
            mkdir(data_dir)
        self.__sql_connect_account = SQLite(data_dir + '\\test_account.sqlite', False)
        self.__sql_connect_resources = SQLite(data_dir + '\\test_resources.sqlite', False)
        # создать таблицу если её нету:
        SQLite.exec_query(self.__sql_connect_account, Const.NEW_TABLE_ACCOUNTS.value)

    def ui_init(self, name_and_version: tuple):
        """Запуск всего UI в консоли и дальнейшая работа в ней."""
        #
        self.__windows = Windows(name_and_version)
        #
        while True:
            Console.clear()
            # отрисуем окно в консоли
            match self.__windows.get_window():
                case GConst.WIN_MANUAL.value:
                    self.__windows.window_manual()
                case GConst.WIN_AUTHENTICATION.value:
                    self.__windows.window_authentication()
                case GConst.WIN_REGISTRATION.value:
                    self.__windows.window_registration()
                case GConst.WIN_LOGIN.value:
                    self.__windows.window_login()
                case GConst.WIN_MAIN_MENU.value:
                    self.__windows.window_main_menu()
                case GConst.WIN_ADD_RESOURCE.value:
                    self.__windows.window_add_resource()
                case GConst.WIN_VIEW_RESOURCE.value:
                    self.__windows.window_view_resource()
                case GConst.WIN_EXIT.value:
                    # завершаем работу с приложением здесь...
                    break
            #
            # отработаем по запросам к БД, если таковы имеются
            args_for_query = self.__windows.get_query()
            match args_for_query[0]:
                # регистрация аккаунта в сейфе, успешно ли зарегало? или уже есть такой акк?
                case GConst.QUERY_REGISTRATION.value:
                    result_account = SQLite.exec_read_query(
                        self.__sql_connect_account,
                        'SELECT name FROM users WHERE name = ?',
                        (args_for_query[1],),
                    )
                    # если такого аккаунта нету - создаём новую запись в одну БД
                    # и новую таблицу в другую БД
                    if result_account == []:
                        SQLite.exec_query(
                            self.__sql_connect_account,
                            'INSERT INTO users (name, pass) VALUES (?, ?)',
                            args_for_query[1:4],
                        )
                        SQLite.exec_query(
                            self.__sql_connect_resources,
                            'CREATE TABLE IF NOT EXISTS '
                            + args_for_query[1]
                            + Const.NEW_TABLE_RESOURCES.value,
                        )
                        self.__windows.set_window(
                            GConst.WIN_AUTHENTICATION.value,
                            'Аккаунт с именем '
                            + args_for_query[1]
                            + ' успешно зарегистрирован в базе, теперь можно войти.',
                        )
                    else:
                        self.__windows.set_window(
                            GConst.WIN_AUTHENTICATION.value,
                            'Аккаунт с именем '
                            + args_for_query[1]
                            + ' уже зарегистрирован в базе, придумайте себе другое имя!',
                        )
                #
                case GConst.QUERY_LOGIN.value:
                    result_account = SQLite.exec_read_query(
                        self.__sql_connect_account,
                        'SELECT name, pass FROM users WHERE name = ? AND pass = ?',
                        args_for_query[1:3],
                    )
                    # если такого аккаунта нету - не впускаем и предупреждаем почему
                    if result_account == []:
                        self.__windows.set_window(
                            GConst.WIN_AUTHENTICATION.value, 'Неверно указан логин или пароль.'
                        )
                    else:
                        result_res = SQLite.exec_read_query(
                            self.__sql_connect_resources, 'SELECT * FROM ' + result_account[0][0]
                        )
                        self.__account = AccountData(
                            result_account[0][0], result_account[0][1], result_res
                        )
                        self.__windows.sync_account(self.__account)
                        self.__windows.set_window(GConst.WIN_MAIN_MENU.value)
                # добавить новый ресурс(имя-логин-пароль)
                case GConst.QUERY_ADD_RESOURCE.value:
                    temp_data = self.__account.get_user_data()
                    next_id = 1
                    if temp_data != []:
                        next_id = temp_data[-1][0] + 1
                    # id, resname, login, pass
                    temp_data.append([next_id, *args_for_query[1:4]])
                    self.__account.set_user_data(temp_data)
                    SQLite.exec_query(
                        self.__sql_connect_resources,
                        'INSERT INTO '
                        + self.__account.get_user_name()
                        + ' (id, resource, login, pass) VALUES (?, ?, ?, ?)',
                        (next_id, *args_for_query[1:4])
                    )
                # ! удалить выбранный ресурс
                case GConst.QUERY_DEL_RESOURCE.value:
                    resource = args_for_query[1]
                    # ? удалить с кеша
                    temp_data = self.__account.get_user_data()
                    temp_data.remove(resource)
                    # self.__account.set_user_data(temp_data)
                    # удалить с БД
                    SQLite.exec_query(
                        self.__sql_connect_resources,
                        'DELETE FROM ' + self.__account.get_user_name() + ' WHERE id = ?',
                        (resource[0],),
                    )
                    # обновить окно, так как сперва обновляются окна, потом выполняются запросы
                    self.__windows.update_window()
