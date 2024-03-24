"""Модуль для работы с хэшем."""

import hashlib
from os import mkdir, getcwd
from os.path import isdir


def get_hash(value: str, code="utf-8", algo_type="sha512") -> str:
    """Получить хэш значение для указанной строки.

    Args:
        value (str): значение для получения хэша
        code (str): кодировка для конвертации value
        algo_type (str): алгоритм хэширования

    Returns:
        str: Хэшированное значение
    """
    hash_temp = hashlib.new(algo_type)
    text_byte = value.encode(code)
    hash_temp.update(text_byte)
    return hash_temp.hexdigest()


def make_path(path: str) -> None:
    """Проложить путь, создать нужные папки

    Args:
        path (str): директория для создания папок
    """
    path_parts = path.split('/')
    current_path = getcwd()
    for part in path_parts:
        if not isdir(current_path + '/' + part):
            mkdir(current_path + '/' + part)
        current_path = current_path + '/' + part


# def contains_char_in_digits(self, string: str) -> bool:
#     """Проверка строки на то, что в ней по мимо цифр есть символы."""
#     for char in string:
#         if not char.isdigit():
#             return True
#     return False
