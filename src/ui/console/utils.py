class Console:
    """Библиотека для работы с консолью."""

    def clear():
        """Имитация очистки консоли."""
        print("\033[H\033[J")

    def error(string):
        """Сообщение об ошибке, вывод красного текста в консоль."""
        print(f"\033[31m[ОШИБКА] {string}\033[0m")

    def warn(string):
        """Сообщение о предупреждении, вывод жёлтого текста в консоль."""
        if string == "" or string == "\n":
            print("")
        else:
            print(f"\033[33m[ВНИМАНИЕ] {string}\033[0m")

    def succes(string):
        """Сообщение об успехе, вывод зелёного текста в консоль."""
        print(f"\033[32m[УСПЕХ] {string}\033[0m")

    def message(string):
        """Простое сообщение, вывод бирюзового текста в консоль."""
        print(f"\033[36m{string}\033[0m")


class Other:
    """Библиотека с разными инструментами."""

    def contains_char_in_digits(string):
        """Проверка строки на то, что в ней по мимо цифр есть символы."""
        for char in string:
            if not char.isdigit():
                return True
        return False
