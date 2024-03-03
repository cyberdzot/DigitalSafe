from controller.core import Core

APP_NAME = "Digital Safe"
APP_VERSION = "0.4.0"


# ! сделать логирование, разобраться почему не запускается в экзешнике
def main():
    """Точка входа."""
    Core().run_application((APP_NAME, APP_VERSION))


if __name__ == "__main__":
    main()
