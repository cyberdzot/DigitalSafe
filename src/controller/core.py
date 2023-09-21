from controller.core_consts import Const
from utils.console import Console
from os import path, mkdir
from db.data_base_sqlite import SQLite

class Core():
    """Ядро программы(Контроллер)."""

    def db_init(self):
        """Инициализация базы данных на старте программы."""
        data_dir = path.dirname(path.realpath(__file__)) + '\\data'
        if not path.isdir(data_dir):
            mkdir(data_dir)
        self.sql_connect = SQLite(data_dir + '\\test.sqlite', True)
        # создать таблицу если её нету:
        SQLite.exec_query(self.sql_connect, Const.Q_NEW_TABLE.value)


    def start_program(self):
        """Запуск программы."""
        Console.clear()
        self.db_init()
        # TODO: начать писать консольный интерфейс
        # записать значения:
        # SQLite.exec_query(sql_connect, Const.Q_ADD_USERS.value) 
        # достать данные из базы:
        users = SQLite.exec_read_query(self.sql_connect, Const.Q_SELECT_USERS.value)
        for user in users:
            Console.message(user)
