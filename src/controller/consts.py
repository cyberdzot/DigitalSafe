from enum import Enum


class Const(Enum):
    """Константные значения для модулей 'controller'."""

    # запрос для создания таблицы 'users'
    Q_NEW_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        pass TEXT NOT NULL
    );
    """
