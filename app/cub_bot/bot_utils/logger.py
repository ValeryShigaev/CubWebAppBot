""" Настройка и инстанс логгера """

import logging

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="bot_debug.log",
                    filemode="w",
                    format=Log_Format,
                    level=logging.ERROR)
logger = logging.getLogger()
