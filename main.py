import sqlite3
from sqlite3 import Error
import utils
# import os


def create_connection(path):
    """Подключить к выбранной БД(SQLite) по указанному пути."""
    connection = None
    try:
        connection = sqlite3.connect(path)
        utils.print_suc("Подключение к БД 'SQLite' - выполнено.")
    except Error as e:
        utils.print_err(f"Подключение к БД 'SQLite' - ошибка: '{e}'.")

    return connection


def execute_query(connection, query):
    """Выполнить SQL запрос к указанному соединению."""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        utils.print_suc(f"Запрос:\n{query}\nвыполнен - успешно.")
    except Error as e:
        utils.print_err(f"Запрос:\n{query}\nне выполнен - ошибка: '{e}'.")


create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    pass TEXT NOT NULL
);
"""
create_users = """
INSERT INTO
    users (login, pass)
VALUES
    ('Vova', '123'),
    ('Han', '456');
"""
select_users = "SELECT * FROM users"


# Не рекомендуется использовать 'SELECT *' для больших таблиц,
# так как это может привести к большому числу операций ввода-вывода,
# которые увеличивают сетевой трафик.
def execute_read_query(connection, query):
    """Выполнить SQL запрос к указанному соединению, для чтения данных с БД."""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        utils.print_err(f"Запрос не выполнен - ошибка: '{e}'.")


if __name__ == '__main__':
    utils.clear_console()
    # utils.print_ds(__file__)
    # current_file = os.path.realpath(__file__)
    # current_directory = os.path.dirname(current_file)

    # подключились к БД
    connection = create_connection('test.sqlite')

    # создали таблицу
    execute_query(connection, create_users_table)

    # записали значения
    # execute_query(connection, create_users)

    # прочитали значения
    users = execute_read_query(connection, select_users)
    for user in users:
        utils.print_ds(user)
