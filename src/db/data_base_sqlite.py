"""Модуль, отвечающий за работу с SQLite."""

from sqlite3 import connect, Error
from db.data_base import DataBase  # pylint:disable=E0401
from utils.utils_consts import ConstDB  # pylint:disable=E0401


class SQLite(DataBase):
    """Класс содержащий поведение и атрибуты для SQLite."""

    def __init__(self, path: str, logger, log_name: str, log_level: int):
        """Инициализация и подключение базы данных."""
        # super().__init__()
        self.__logger = logger
        self.__log_name = log_name
        try:
            self.__log_level = log_level
            self.__connection = connect(path)
            if log_level == ConstDB.LOG_3_ALL.value:
                logger.debug(
                    f"[{log_name}] Подключение к БД 'SQLite' - выполнено.")
        except Error as error:
            if log_level >= ConstDB.LOG_2_ERROR.value:
                logger.error(
                    f"[{log_name}] Подключение к БД 'SQLite' - ошибка: {error}.")

    def exec_query(self, query: str, args=()) -> None:
        """Выполнение SQL запроса без возвращения значений."""
        # super().exec_query()
        cursor = self.__connection.cursor()
        try:
            if args == ():
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            self.__connection.commit()
            if self.__log_level == ConstDB.LOG_3_ALL.value:
                self.__logger.debug(
                    f"[{self.__log_name}] Запрос:\n{query}\nвыполнен - успешно.")
        except Error as error:
            if self.__log_level >= ConstDB.LOG_2_ERROR.value:
                self.__logger.error(
                    f"[{self.__log_name}] Запрос:\n{query}\nне выполнен - ошибка: {error}.")

    def exec_read_query(self, query: str, args=()) -> (list | None):
        """Выполнение SQL запроса с возвращяемыми значениями."""
        # super().exec_read_query()
        cursor = self.__connection.cursor()
        try:
            if args == ():
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            if self.__log_level == ConstDB.LOG_3_ALL.value:
                self.__logger.debug(
                    f"[{self.__log_name}] Запрос:\n{query}\nвыполнен - успешно.")
            return cursor.fetchall()
        except Error as error:
            if self.__log_level >= ConstDB.LOG_2_ERROR.value:
                self.__logger.error(
                    f"[{self.__log_name}] Запрос не выполнен - ошибка: {error}.")
            return None
