"""Модуль с констатами для глобальной части проекта."""

from enum import Enum, auto


class GConst(Enum):
    """Глобальные автоматически пронумерованные константы."""

    # список окон (WIN = WINDOW)
    WIN_EXIT = auto()
    WIN_MANUAL = auto()
    WIN_WAITING = auto()
    WIN_MAIN_MENU = auto()
    WIN_ADD_RESOURCE = auto()
    WIN_VIEW_RESOURCE = auto()
    WIN_AUTHENTICATION = auto()
    WIN_REGISTRATION = auto()
    WIN_LOGIN = auto()

    QUERY_REGISTRATION = auto()
    QUERY_LOGIN = auto()
    QUERY_ADD_RESOURCE = auto()
    QUERY_DEL_RESOURCE = auto()
