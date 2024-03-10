"""Модуль, отвечающий за работу с SQLite."""

from db.data_base import DataBase
from utils.utils_console import Console
from sqlite3 import connect, Error


class SQLite(DataBase):
    """Класс содержащий поведение и атрибуты для SQLite."""

    def __init__(self, console: Console, path: str, log_state: bool):
        """Инициализация и подключение базы данных.

        Ключевые аргументы:
        * path - путь к файлу '.sqlite'
        * is_log_suc - выполнять ли логирование успешных запросов в консоль 'True' или 'False'
        """
        self.__console = console
        try:
            self.__log_state = log_state
            self.__connection = connect(path)
            if log_state:
                self.__console.succes("Подключение к БД 'SQLite' - выполнено.")
        except Error as error:
            self.__console.error(
                f"Подключение к БД 'SQLite' - ошибка: {error}.")

    def exec_query(self, query: str, args=()) -> None:
        """Выполнение SQL запроса без возвращения значений."""
        cursor = self.__connection.cursor()
        try:
            if args == ():
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            self.__connection.commit()
            if self.__log_state:
                self.__console.succes(f"Запрос:\n{query}\nвыполнен - успешно.")
        except Error as error:
            self.__console.error(
                f"Запрос:\n{query}\nне выполнен - ошибка: {error}.")

    def exec_read_query(self, query: str, args=()) -> (list | None):
        """Выполнение SQL запроса с возвращяемыми значениями."""
        cursor = self.__connection.cursor()
        try:
            if args == ():
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            if self.__log_state:
                self.__console.succes(f"Запрос:\n{query}\nвыполнен - успешно.")
            return cursor.fetchall()
        except Error as error:
            self.__console.error(f"Запрос не выполнен - ошибка: {error}.")
