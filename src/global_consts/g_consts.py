from enum import Enum, auto


class GConst(Enum):
    """Глобальные константы."""

    # список окон
    WIN_EXIT = auto()
    WIN_LOGIN = auto()
    WIN_MANUAL = auto()
    WIN_AUTH = auto()
    WIN_REG = auto()
    WIN_WAITING = auto()

    QUERY_REG = auto()
