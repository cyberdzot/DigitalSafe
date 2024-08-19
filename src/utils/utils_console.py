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

    def error(self, text: str):
        """Сообщение об ошибке, вывод красного текста в консоль."""
        print(f"{Fore.RED}[ОШИБКА] {text}")

    def warn(self, text: str):
        """Сообщение о предупреждении, вывод жёлтого текста в консоль."""
        if text in {"", "\n"}:
            print("")
        else:
            print(f"{Fore.YELLOW}[ВНИМАНИЕ] {text}")

    def succes(self, text: str):
        """Сообщение об успехе, вывод зелёного текста в консоль."""
        print(f"{Fore.GREEN}[УСПЕХ] {text}")

    def message(self, text: str):
        """Простое сообщение, вывод бирюзового/голубого текста в консоль."""
        print(f"{Fore.CYAN}{text}")
