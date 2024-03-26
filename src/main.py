"""Модуль с точкой входа."""

from controller.core import Core

APP_NAME = "Digital Safe"
APP_VERSION = "0.4.2"


def main():
    """Точка входа."""
    Core((APP_NAME, APP_VERSION))


if __name__ == "__main__":
    main()
