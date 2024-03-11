"""Модуль, отвечающий за интерфейс для баз данных."""

from abc import ABC, abstractmethod


class DataBase(ABC):
    """Общее поведение для различных БД."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def exec_query(self):
        """Выполнить SQL запрос к указанному соединению."""

    @abstractmethod
    def exec_read_query(self):
        """Выполнить SQL запрос к указанному соединению, для чтения данных с БД."""
