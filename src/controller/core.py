"""Модуль, отвечающий за контроллер, где происходит основная работа приложения."""

from db.data_base_sqlite import SQLite  # pylint:disable=E0401
from entities.account_data import AccountData  # pylint:disable=E0401
from entities.scrambler import Cipher  # pylint:disable=E0401
from ui.console.windows import ConsoleUI  # pylint:disable=E0401
from utils.utils_consts import ConstAutoNum, ConstCore, ConstDB  # pylint:disable=E0401
from utils.utils_console import Console  # pylint:disable=E0401
from utils.utils_others import make_path  # pylint:disable=E0401
from utils.utils_logger import logger_init  # pylint:disable=E0401


class Core:
    """Ядро программы (Контроллер)."""

    def __init__(self, app_info: tuple):
        # инициализация логгера
        self.__logger = logger_init("logs")

        # инициализация консоли
        self.__console = Console()

        # подключение к базе данных или сначала её инициализация(если первый запуск)
        self.__sql_connect_account = None
        self.__sql_connect_resources = None
        self.db_init()

        # создание шифратора/дешифратора с временным ключём
        # в процессе входа приложим мастер-пароль вместо этого ключа
        self.__cipher = Cipher("0i&2M*2Hsq^rWLt1")

        # запуск интерфейса
        self.__windows = ConsoleUI(
            self.__console, app_info, self.__cipher)
        self.__account = None
        self.ui_launch()

    def db_init(self) -> None:
        """Инициализация базы данных на старте программы."""

        # настраиваем путь к директории БД(если он отсутвует) и открываем соединения с БД
        data_dir = "data"
        make_path(data_dir)
        self.__sql_connect_account = SQLite(
            data_dir + "/accounts.sqlite",
            self.__logger,
            "accounts",
            ConstDB.LOG_2_ERROR.value)
        self.__sql_connect_resources = SQLite(
            data_dir + "/resources.sqlite",
            self.__logger,
            "resources",
            ConstDB.LOG_2_ERROR.value)
        # создаём таблицу аккаунтов если её нету:
        SQLite.exec_query(self.__sql_connect_account,
                          ConstCore.NEW_TABLE_ACCOUNTS.value)

    def ui_launch(self) -> None:
        """Запуск и дальнейшая работа UI в консоли."""
        # Цикл собран под console-ui
        while True:
            self.__console.clear()
            # отрисуем выбранное окно в консоли
            match self.__windows.get_window():
                case ConstAutoNum.WIN_MANUAL.value:
                    self.__windows.window_manual()
                case ConstAutoNum.WIN_AUTHENTICATION.value:
                    self.__windows.window_authentication()
                case ConstAutoNum.WIN_REGISTRATION.value:
                    self.__windows.window_registration()
                case ConstAutoNum.WIN_LOGIN.value:
                    self.__windows.window_login()
                case ConstAutoNum.WIN_MAIN_MENU.value:
                    self.__windows.window_main_menu()
                case ConstAutoNum.WIN_ADD_RESOURCE.value:
                    self.__windows.window_add_resource()
                case ConstAutoNum.WIN_VIEW_RESOURCE.value:
                    self.__windows.window_view_resource()
                case ConstAutoNum.WIN_EXIT.value:
                    # завершаем работу с приложением здесь...
                    break
            # отработаем по запросам к БД, если таковы имеются
            args_for_query = self.__windows.get_query()
            match args_for_query[0]:
                # регистрация аккаунта в сейфе, успешно ли зарегало? или уже есть такой акк?
                case ConstAutoNum.QUERY_REGISTRATION.value:
                    result_account = SQLite.exec_read_query(
                        self.__sql_connect_account,
                        "SELECT name FROM users WHERE name = ?",
                        (args_for_query[1],),
                    )
                    # если такого аккаунта нету - создаём новую запись в одну БД
                    # и новую таблицу в другую БД
                    if result_account == []:
                        SQLite.exec_query(
                            self.__sql_connect_account,
                            "INSERT INTO users (name, pass) VALUES (?, ?)",
                            args_for_query[1:4],
                        )
                        SQLite.exec_query(
                            self.__sql_connect_resources,
                            "CREATE TABLE IF NOT EXISTS "
                            + args_for_query[1]
                            + ConstCore.NEW_TABLE_RESOURCES.value,
                        )
                        self.__windows.set_window(
                            ConstAutoNum.WIN_AUTHENTICATION.value,
                            "Аккаунт с именем "
                            + args_for_query[1]
                            + " успешно зарегистрирован в базе, теперь можно войти.",
                        )
                    else:
                        self.__windows.set_window(
                            ConstAutoNum.WIN_AUTHENTICATION.value,
                            "Аккаунт с именем "
                            + args_for_query[1]
                            + " уже зарегистрирован в базе, придумайте себе другое имя!",
                        )
                case ConstAutoNum.QUERY_LOGIN.value:
                    result_account = SQLite.exec_read_query(
                        self.__sql_connect_account,
                        "SELECT name, pass FROM users WHERE name = ? AND pass = ?",
                        args_for_query[1:3],
                    )
                    # если такого аккаунта нету - не впускаем с предупреждением
                    if result_account == []:
                        self.__windows.set_window(
                            ConstAutoNum.WIN_AUTHENTICATION.value,
                            "Неверно указан логин или пароль.",
                        )
                    else:
                        result_res = SQLite.exec_read_query(
                            self.__sql_connect_resources,
                            "SELECT * FROM " + result_account[0][0],
                        )
                        self.__account = AccountData(
                            result_account[0][0], result_account[0][1], result_res
                        )
                        # делаем мастер-пароль до хеширования ключём для шифратора
                        self.__cipher.set_password(args_for_query[3])
                        self.__windows.sync_account(
                            self.__account)
                        self.__windows.set_window(
                            ConstAutoNum.WIN_MAIN_MENU.value)
                # добавить новый ресурс(имя-логин-пароль)
                case ConstAutoNum.QUERY_ADD_RESOURCE.value:
                    temp_data = self.__account.get_user_data()
                    next_id = 1
                    if temp_data != []:
                        next_id = temp_data[-1][0] + 1
                    # id, *resname, login, pass
                    temp_data.append([next_id, *args_for_query[1:4]])
                    self.__account.set_user_data(temp_data)
                    SQLite.exec_query(
                        self.__sql_connect_resources,
                        "INSERT INTO "
                        + self.__account.get_user_name()
                        + " (id, resource, login, pass) VALUES (?, ?, ?, ?)",
                        (next_id, *args_for_query[1:4]),
                    )
                # удалить выбранный ресурс
                case ConstAutoNum.QUERY_DEL_RESOURCE.value:
                    resource = args_for_query[1]
                    # удалить с кеша
                    temp_data = self.__account.get_user_data()
                    temp_data.remove(resource)
                    # удалить с БД
                    SQLite.exec_query(
                        self.__sql_connect_resources,
                        "DELETE FROM "
                        + self.__account.get_user_name()
                        + " WHERE id = ?",
                        (resource[0],),
                    )
                    # обновить окно, так как по умолчанию сперва обновляются окна,
                    # потом выполняются запросы
                    self.__windows.update_window()
