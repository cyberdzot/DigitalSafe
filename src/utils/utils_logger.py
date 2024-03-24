"""Модуль, отвечающий за инициализацию логгера."""

import logging
from utils.utils_others import make_path  # pylint:disable=E0401


def logger_init(file_name: str):
    """Создать логгер.

    Args:
        file_name (str): название файла в который логгер будет делать записи.

    Returns:
        Logger: Получить логгер.
    """
    logs_dir = "logs"
    make_path(logs_dir)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                        filename=f'{logs_dir}/{file_name}.log', filemode='a', encoding='utf-8')
    log = logging.getLogger(__name__)
    return log


# logger = logger_init('my_log')
# logger.error('debuggggg')
