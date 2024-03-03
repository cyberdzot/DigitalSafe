import hashlib


class Hash:
    def __init__(self, code="utf-8", algo_type="sha512"):
        self.__code = code
        self.__hash = hashlib.new(algo_type)

    def get(self, value: str) -> str:
        text_byte = value.encode(self.__code)
        self.__hash.update(text_byte)
        return self.__hash.hexdigest()


# пример
# hash = Hash()
# print(hash.get('!?3ЛWsы%*()'))
