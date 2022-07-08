from typing import Dict, Union

from ..models import Employee, Note, Object
from .decorators import error_handler
from .logger import logger


class BotDBManager:
    """
    Класс, инкапсулирующий работу с БД

    Методы:
    remove_worker - удаление работника
    add_worker - добавление работника
    remove_object - удаление объекта
    add_object - добавление объекта
    add_note - добавление записи
    remove_note - удаление записи
    generate_report - генерация отчета
    result_struct - создание структурированного словаря для отчета
    """

    @classmethod
    @error_handler
    def remove_worker(cls, idx: int) -> bool:
        """
        Удаление работника

        :param idx: id работника
        :type idx: int
        :rtype: bool
        """

        worker = Employee.objects.get(id=idx)
        worker.deleted = True
        worker.save()
        return True

    @classmethod
    @error_handler
    def add_worker(cls, name: str) -> bool:
        """
        Добавление работника

        :param name: name работника
        :type name: str
        :rtype: bool
        """

        Employee.objects.get_or_create(name=name, deleted=False)
        return True

    @classmethod
    @error_handler
    def remove_object(cls, idx):
        """
        Удаление объекта

        :param idx: id объекта
        :type idx: int
        :rtype: bool
        """

        obj = Object.objects.get(id=idx)
        obj.deleted = True
        obj.save()
        return True

    @classmethod
    @error_handler
    def add_object(cls, name: str, tariff: int):
        """
        Добавление объекта

        :param name: name объекта
        :type name: str
        :param tariff: tariff объекта
        :type tariff: int
        :rtype: bool
        """

        Object.objects.get_or_create(name=name, tariff=tariff,
                                     deleted=False)
        return True

    @classmethod
    def add_note(cls, data: Dict) -> Union[str, None]:
        """
        Добавление записи, не вернет ничего если запись добавлена,
        вернет строку ошибки если такой шурф уже есть

        :param data: словарь из запроса
        :type data: dict
        :rtype: str, None
        """

        try:
            if list(Note.objects.filter(pit_number=data["pit_number"],
                                        obj=data["object"],
                                        deleted=False)):
                return data["tg_idx"]
            price = (float(data["pit_depth"]) * int(data["pitsize"]) *
                     Object.objects.get(id=data["object"]).tariff)
            new_note = Note.objects.create(
                tg_idx=data["tg_idx"],
                obj=Object.objects.get(id=data["object"]),
                pit_number=data["pit_number"],
                pit_depth=data["pit_depth"],
                pit_size=data["pitsize"],
                price=price
            )
            for name in data["names"]:
                print(name)
                new_note.names.add(Employee.objects.get(id=name))
                new_note.save()
            return None
        except Exception as e:
            logger.error(e)
            return "Непредвиденная ошибка"

    @classmethod
    @error_handler
    def remove_note(cls, idx: int):
        """
        Удаление записи

        :param idx: id записи
        :type idx: int
        :rtype: bool
        """

        note = Note.objects.get(id=idx)
        note.deleted = True
        note.save()
        return True

    @classmethod
    def generate_report(cls, data: Dict) -> Union[Dict, str]:
        """
        Возвращает отчет или ошибку

        :param data: словарь из запроса
        :type data: dict
        :rtype: dict, str
        """

        try:
            return cls.result_struct(data)
        except Exception as e:
            logger.error(e)
            return "Непредвиденная ошибка"

    @classmethod
    def result_struct(cls, data) -> Dict:
        """
        Создание структурированного словаря для отчета,
        возможности рендеринга отчета на веб-странице

        :param data: словарь из запроса
        :type data: dict
        :rtype: dict
        """

        result = dict()
        notes = Note.objects.filter(crated_at__range=[data["from"],
                                                      data["to"]],
                                    deleted=False).prefetch_related("names")
        for note in notes:
            pit_number = note.pit_number
            price = note.price if len(list(note.names.all())) == 1 else\
                round(note.price / len(list(note.names.all())), 2)
            for name in note.names.all():
                if name.name in result.keys():
                    if note.obj.name in result[name.name].keys():
                        result[name.name][note.obj.name]["pits"].\
                            append(pit_number)
                        result[name.name][note.obj.name]["prices"].\
                            append(price)
                        result[name.name][note.obj.name]["total"] += price
                    else:
                        result[name.name][note.obj.name] = \
                            {"pits": [pit_number],
                             "prices": [price],
                             "total": price}
                else:
                    result[name.name] = {note.obj.name: {"pits": [pit_number],
                                                         "prices": [price],
                                                         "total": price},
                                         "total": 0}
        for key in result.keys():
            for k in result[key].keys():
                if k != "total":
                    result[key]["total"] += result[key][k]["total"]
        return result


