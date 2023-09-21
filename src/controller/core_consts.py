from enum import Enum


class Const(Enum):
    """Класс констант."""

    # запрос для создания таблицы 'users'
    Q_NEW_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        pass TEXT NOT NULL
    );
    """

    Q_ADD_USERS = """
    INSERT INTO
        users (login, pass)
    VALUES
        ('Vova', '123'),
        ('Han', '456');
    """

    Q_SELECT_USERS = "SELECT * FROM users;"
