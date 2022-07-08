from typing import Dict, Union

from django.contrib.auth import authenticate, login
from django.http import HttpRequest, QueryDict

from .bot_db_manager import BotDBManager
from .logger import logger

db_manager = BotDBManager()


def querydict_to_dict(qdict: QueryDict) -> Dict[str, any]:
    """
    Конвертирует Django QueryDict в словарь

    :param qdict: Входящий QueryDict
    :type qdict: QueryDict
    :rtype: dict[str, any]
    """

    return {key: value for key, value in qdict.items()}


def request_handler(request: QueryDict) -> Dict[str, str]:
    """
    Обрабатывает все запросы, генерирует часть контекста,
    основное - название пункта меню для перехода,
    телеграм id юзера

    :param request: Входящий QueryDict
    :type request: QueryDict
    :rtype: dict[str, str]
    """

    context = dict()
    data = querydict_to_dict(request)
    data_keys = list(data.keys())
    if "section" in data_keys:
        context["select"] = data["section"]
    else:
        context["select"] = "main"
    if "tg_idx" in data_keys:
        context["tg_idx"] = data["tg_idx"]
    return context


def db_controller(request: QueryDict) -> Union[bool, str]:
    """
    Производит работу с БД в зависимости от ключей запроса
    Может вернуть текст ошибки если она произойдет на стороне БД

    Отвечает за:
    Добавление работника
    Удаление работника
    Добавление объекта
    Удаление объекта
    Удаление записи

    :param request: Входящий QueryDict
    :type request: QueryDict
    :rtype: bool, str
    """

    data = querydict_to_dict(request)
    data_keys = list(data.keys())
    if "names" in data_keys:
        data["names"] = request.getlist("names")
    if "add_worker" in data_keys:
        return db_manager.add_worker(data["add_worker"])
    if "remove_worker" in data_keys:
        return db_manager.remove_worker(data["remove_worker"])
    if "remove_object" in data_keys:
        return db_manager.remove_object(data["remove_object"])
    if "add_object" in data_keys:
        return db_manager.add_object(data["add_object"], data["add_tariff"])
    if "remove_note" in data_keys:
        return db_manager.remove_note(data["remove_note"])


def add_note_controller(request: QueryDict) -> Union[str, bool]:
    """
    Добавляет запись. Может вернуть текст
    если такие данные уже есть или произошла ошибка

    :param request: Входящий QueryDict
    :type request: QueryDict
    :rtype: bool, str
    """

    data = querydict_to_dict(request)
    data_keys = list(data.keys())
    if "pitsize" in data_keys:
        data["names"] = request.getlist("names")
        return db_manager.add_note(data)
    return False


def login_controller(request: HttpRequest) -> Union[bool, str]:
    """
    Полуручной логин. Выдает True если все нормально,
    False при ошибке, строку при несоответствии данных

    :param request: Входящий HttpRequest
    :type request: HttpRequest
    :rtype: bool, str
    """

    if request.GET.get("login"):
        log = request.GET.get("login")
        password = request.GET.get("pass")
        try:
            user = authenticate(username=log, password=password)
            login(request, user)
            return True
        except Exception as e:
            logger.error(e)
            return False
    return "No data"


def data_to_report(request: QueryDict) -> Union[Dict, None]:
    """
    Делает отчет из данных ключей запроса. Вернет отчет, или ничего.

    :param request: Входящий QueryDict
    :type request: QueryDict
    :rtype: dict, none
    """

    data = querydict_to_dict(request)
    data_keys = list(data.keys())
    if "names" in data_keys:
        data["names"] = request.getlist("names")
    if "from" in data_keys:
        return db_manager.generate_report(data)
    return None
