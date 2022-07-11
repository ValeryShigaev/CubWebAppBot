from typing import Dict, Union

from django.http import HttpRequest, QueryDict
from django.shortcuts import render
from django.views import View

from .bot_utils.request_handlers import (add_note_controller, data_to_report,
                                         db_controller, login_controller,
                                         request_handler)
from .models import Employee, Note, Object


class BotMenuView(View):

    def get(self, request: HttpRequest):
        """
        На get из запроса генерируется часть контекста,
        данные запроса проходят через обработчик, записывается error если
        обработчик его выкидывает, генерируется queryset, работает логин

        Get отвечает за:
        Удаление записи
        Удаление объекта
        Удаление работника
        Создание объекта
        Создание рабоника
        Переход по меню
        Логин
        """

        mod_data = self.querydict_to_dict(request.GET)
        names = (request.getlist("names") if "names" in mod_data.keys()
                 else None)
        context = request_handler(mod_data)
        result = db_controller(mod_data, names)
        error = result if isinstance(result, str) else ""
        queryset = self.generate_queryset(request.GET.get("tg_idx"))
        log_data = login_controller(request)
        context = {**queryset, **context, **{"log_error": log_data,
                                             "error": error}}
        return render(request, 'management/bot/bot_management.html', context)

    def post(self, request: HttpRequest):
        """
        На post работает создание отчета и добавление записи

        Post отвечает за:
        Генерацию и рендеринг отчета
        Добавление записи в БД
        """

        queryset = self.generate_queryset()
        report = data_to_report(request.POST)
        mod_data = self.querydict_to_dict(request.POST)
        names = (request.POST.getlist("names") if "names" in mod_data.keys()
                 else None)
        if report:
            error = report if isinstance(report, str) else ""
            return render(request, 'management/bot/bot_management.html',
                          {**{"select": "report", "report": report,
                              "error": error}, **queryset})
        answer = add_note_controller(mod_data, names)
        if answer:
            return render(request, 'management/bot/bot_management.html',
                          {**{"select": "note", "error": self.err_text(answer),
                              "tg_idx": answer}, **queryset})
        return render(request, 'management/bot/bot_management.html',
                      {**{"select": "main", "check": True}, **queryset})

    def generate_queryset(self, tg_idx: int = 0) -> Dict:
        """
        Здесь генерируются queryset's работников, объектов, записей

        :param tg_idx: телеграм id юзера
        :type tg_idx: int
        :rtype: Dict
        """

        names = {"names": ([item for item in
                            Employee.objects.filter(deleted=False)])}
        objects = {"objects": ([obj for obj in
                                Object.objects.filter(deleted=False)])}
        notes = {"notes": ([note for note in
                            Note.objects.filter(tg_idx=tg_idx,
                                                deleted=False).order_by(
                                "crated_at")][10::-1])}
        return {**names, **objects, **notes}


    @classmethod
    def err_text(cls, answer: Union[str, None]) -> str:
        """
        Метод для возврата определенной ошибки при добавлении записи,
        если обработчиком будет возвращен id юзера - такие данные уже есть,
        иначе будет возвращена ошибка записи в БД

        :param answer: Ответ обработчика записи данных в БД
        :type answer: str, None
        :rtype: str
        """

        if answer[0].isdigit():
            return "Такие данные уже есть"
        else:
            return answer

    @staticmethod
    def querydict_to_dict(qdict: QueryDict) -> Dict[str, any]:
        """
        Конвертирует Django QueryDict в словарь

        :param qdict: Входящий QueryDict
        :type qdict: QueryDict
        :rtype: dict[str, any]
        """

        return {key: value for key, value in qdict.items()}
