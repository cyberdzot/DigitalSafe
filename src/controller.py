from src.utils import Console
from src.data_base_sqlite import SQLite
# import os


# Не рекомендуется использовать 'SELECT *' для больших таблиц,
# так как это может привести к большому числу операций ввода-вывода,
# которые увеличивают сетевой трафик.
q_new_table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    pass TEXT NOT NULL
);
"""
q_add_users = """
INSERT INTO
    users (login, pass)
VALUES
    ('Vova', '123'),
    ('Han', '456');
"""
q_select_users = "SELECT * FROM users;"


def start_program():
    Console.clear()
    # Console.message(__file__)                         # полный путь к файлу
    # current_file = os.path.realpath(__file__)
    # current_directory = os.path.dirname(current_file)

    sql_connect = SQLite('test.sqlite', False)          # подключились к БД
    # Console.message(sql_connect.__dict__)             # проверим какие атрибуты у этого класса существуют
    SQLite.exec_query(sql_connect, q_new_table)      # создали таблицу
    # SQLite.exec_query(sql_connect, q_add_users)    # записали значения

    # достали данные из базы
    users = SQLite.exec_read_query(sql_connect, q_select_users)
    for user in users:
        Console.message(user)


if __name__ == '__main__':
    start_program()
