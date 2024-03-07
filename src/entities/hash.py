"""Модуль для работы с хэшем."""

import hashlib


def get_hash(value: str, code="utf-8", algo_type="sha512") -> str:
    """Получить хэш значение для указанной строки."""
    hash_temp = hashlib.new(algo_type)
    text_byte = value.encode(code)
    hash_temp.update(text_byte)
    return hash_temp.hexdigest()


# class Hash:
#     """Инициализация хэш алгоритма."""

#     def __init__(self, code="utf-8", algo_type="sha512"):
#         """Инициализация хэш алгоритма."""
#         self.__code = code
#         self.__hash = hashlib.new(algo_type)

#     def get(self, value: str) -> str:
#         """Получить хэш значение для указанной строки."""
#         text_byte = value.encode(self.__code)
#         self.__hash.update(text_byte)
#         return self.__hash.hexdigest()


# пример
# hash = Hash()
# print(hash.get('!?3ЛWsы%*()'))
