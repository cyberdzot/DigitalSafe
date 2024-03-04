from db.data_base import DataBase
from ui.console.utils import Console
from sqlite3 import connect, Error


class SQLite(DataBase):
    """Класс содержащий поведение и атрибуты для SQLite."""

    def __init__(self, console: Console, path: str, is_log_suc: bool):
        """Инициализация и подключение базы данных.

        Ключевые аргументы:
        * path - путь к файлу '.sqlite'
        * is_log_suc - выполнять ли логирование успешных запросов в консоль 'True' или 'False'
        """
        self.__console = console
        try:
            self.__is_log_suc = is_log_suc
            self.__connection = connect(path)
            if is_log_suc:
                self.__console.succes("Подключение к БД 'SQLite' - выполнено.")
        except Error as error:
            self.__console.error(f"Подключение к БД 'SQLite' - ошибка: {error}.")

    def exec_query(self, query: str, args=()):
        """Выполнение SQL запроса без возвращения значений."""
        cursor = self.__connection.cursor()
        try:
            if args == ():
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            self.__connection.commit()
            if self.__is_log_suc:
                self.__console.succes(f"Запрос:\n{query}\nвыполнен - успешно.")
        except Error as error:
            self.__console.error(f"Запрос:\n{query}\nне выполнен - ошибка: {error}.")

    def exec_read_query(self, query: str, args=()):
        """Выполнение SQL запроса с возвращяемыми значениями."""
        cursor = self.__connection.cursor()
        try:
            if args == ():
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            if self.__is_log_suc:
                self.__console.succes(f"Запрос:\n{query}\nвыполнен - успешно.")
            return cursor.fetchall()
        except Error as error:
            self.__console.error(f"Запрос не выполнен - ошибка: {error}.")
