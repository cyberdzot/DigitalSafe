"""Модуль для работы с хэшем."""

import hashlib


def get_hash(value: str, code="utf-8", algo_type="sha512") -> str:
    """Получить хэш значение для указанной строки."""
    hash_temp = hashlib.new(algo_type)
    text_byte = value.encode(code)
    hash_temp.update(text_byte)
    return hash_temp.hexdigest()

# def contains_char_in_digits(self, string: str) -> bool:
#     """Проверка строки на то, что в ней по мимо цифр есть символы."""
#     for char in string:
#         if not char.isdigit():
#             return True
#     return False
