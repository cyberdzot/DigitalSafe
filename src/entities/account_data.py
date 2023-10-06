class AccountData():
    """Сущность пользователя и его учётных данных."""

    def __init__(self, username: str, password: str, data: list):
        self.__username = username
        self.__userpass = password
        self.__userdata = data

    def get_user_name(self) -> str:
        """Получить имя пользователя."""
        return self.__username

    def get_user_pass(self) -> str:
        """Получить пароль пользователя."""
        return self.__userpass

    def get_user_data(self) -> list:
        """Получить учётные данные пользователя."""
        return self.__userdata

    def set_user_data(self, data: list):
        """Заменить учётные данные пользователя на новые."""
        self.__userdata = data