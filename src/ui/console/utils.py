"""Модуль, отвечающий за форматирование текста и другие функции в консоли."""

from os import system
from colorama import init, Fore


class Console:
    """Библиотека для работы с консолью."""

    def __init__(self):
        init(autoreset=True)

    def clear(self):
        """Имитация очистки консоли."""
        system("cls")

    def error(self, string: str):
        """Сообщение об ошибке, вывод красного текста в консоль."""
        print(f"{Fore.RED}[ОШИБКА] {string}")

    def warn(self, string: str):
        """Сообщение о предупреждении, вывод жёлтого текста в консоль."""
        if string == "" or string == "\n":
            print("")
        else:
            print(f"{Fore.YELLOW}[ВНИМАНИЕ] {string}")

    def succes(self, string: str):
        """Сообщение об успехе, вывод зелёного текста в консоль."""
        print(f"{Fore.GREEN}[УСПЕХ] {string}")

    def message(self, string: str):
        """Простое сообщение, вывод бирюзового/голубого текста в консоль."""
        print(f"{Fore.CYAN}{string}")


# class Other:
#     """Библиотека с разными инструментами."""

#     def contains_char_in_digits(self, string: str) -> bool:
#         """Проверка строки на то, что в ней по мимо цифр есть символы."""
#         for char in string:
#             if not char.isdigit():
#                 return True
#         return False
