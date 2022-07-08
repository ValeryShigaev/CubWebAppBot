from typing import Callable

from .logger import logger


def error_handler(func: Callable) -> Callable:
    """
    Декоратор для отлова ошибок работы с БД,
    логгирования и уведомления пользователя об ошибке

    :param func: метод
    :type func: Callable
    :rtype: Callable
    """

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            return "Непредвиденная ошибка"
    return wrapper
