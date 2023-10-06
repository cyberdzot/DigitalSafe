from enum import Enum


class Const(Enum):
    """Константные значения для модулей 'controller'."""

    # запрос для создания таблицы 'users'
    NEW_TABLE_ACCOUNTS = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        pass TEXT NOT NULL
    )
    """

    # часть запроса для создания таблицы пользователя
    NEW_TABLE_RESOURCES = """
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource TEXT NOT NULL,
        login TEXT NOT NULL,
        pass TEXT NOT NULL
    )
    """
