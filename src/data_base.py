from abc import ABC, abstractmethod


class DB(ABC):
    """Абстрактный класс содержащий общее поведение для различных БД."""

    @abstractmethod
    def __init__(self):
        """Инициализация и подключение базы данных."""
        pass

    @abstractmethod
    def exec_query(self):
        """Выполнить SQL запрос к указанному соединению."""
        pass

    @abstractmethod
    def exec_read_query(self):
        """Выполнить SQL запрос к указанному соединению, для чтения данных с БД."""
        pass
