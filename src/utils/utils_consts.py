"""Модуль с констатами для глобальной части проекта."""

from enum import Enum, auto


class ConstAutoNum(Enum):
    """Глобальные автоматически пронумерованные константы."""

    # список окон (WIN = WINDOW)
    WIN_EXIT = auto()
    WIN_MANUAL = auto()
    WIN_WAITING = auto()
    WIN_MAIN_MENU = auto()
    WIN_ADD_RESOURCE = auto()
    WIN_VIEW_RESOURCE = auto()
    WIN_AUTHENTICATION = auto()
    WIN_REGISTRATION = auto()
    WIN_LOGIN = auto()

    QUERY_REGISTRATION = auto()
    QUERY_LOGIN = auto()
    QUERY_ADD_RESOURCE = auto()
    QUERY_DEL_RESOURCE = auto()


class ConstCore(Enum):
    """Константные значения для модулей 'controller'."""

    # запрос для создания таблицы 'users'
    NEW_TABLE_ACCOUNTS = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        pass TEXT NOT NULL
    )
    """

    # часть запроса для создания таблицы с ресурсами для пользователя
    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    NEW_TABLE_RESOURCES = """
    (
        id INTEGER PRIMARY KEY,
        resource TEXT NOT NULL,
        login TEXT NOT NULL,
        pass TEXT NOT NULL
    )
    """


class ConstDB(Enum):
    """Константные значения для модулей 'db'."""

    LOG_1_OFF = auto()
    LOG_2_ERROR = auto()
    LOG_3_ALL = auto()


class ConstUI(Enum):
    """Константные значения для модулей 'ui'."""

    QUERY_NULL = (None, None, None, None)
