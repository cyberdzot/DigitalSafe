from db.data_base import DB
from utils.console import Console
import sqlite3


class SQLite(DB):
    """Класс содержащий поведение и атрибуты для SQLite."""

    def __init__(self, path, is_log_suc):
        """Инициализация и подключение базы данных.
    
        Ключевые аргументы:
        * path - путь к файлу '.sqlite'
        * is_log_suc - выполнять ли логирование в консоль 'True' или 'False'"""
        try:
            self.__is_log_suc = is_log_suc
            self.__connection = sqlite3.connect(path)
            if is_log_suc:
                Console.succes("Подключение к БД 'SQLite' - выполнено.")
        except sqlite3.Error as e:
            Console.error(f"Подключение к БД 'SQLite' - ошибка: {e}.")

    def exec_query(self, query):
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query)
            self.__connection.commit()
            if self.__is_log_suc:
                Console.succes(f"Запрос:\n{query}\nвыполнен - успешно.")
        except sqlite3.Error as error:
            Console.error(f"Запрос:\n{query}\nне выполнен - ошибка: {error}.")

    def exec_read_query(self, query):
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query)
            if self.__is_log_suc:
                Console.succes(f"Запрос:\n{query}\nвыполнен - успешно.")
            return cursor.fetchall()
        except sqlite3.Error as error:
            Console.error(f"Запрос не выполнен - ошибка: {error}.")
