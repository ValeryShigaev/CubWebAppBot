from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Note, Employee, Object


class MenuTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.name = Employee.objects.create(name="Name2")
        cls.obj = Object.objects.create(name="Object2", tariff=1500)
        cls.user = User.objects.create(email="test@ru.ru",
                                       password="admin732",
                                       first_name="test1")

    def test_block_if_not_telegram(self):
        response = self.client.get("")
        self.assertContains(response, "Sorry!")

    def test_create_worker(self):
        response = self.client.get("?add_worker=Name1&section=employee")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list(obj.name for obj in Employee.objects.all()))
                          , 2)

    def test_remove_worker(self):
        response = self.client.get("?remove_worker=2&section=employee")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list(obj for obj in Employee.objects.filter(
            deleted=False))), 1)

    def test_create_object(self):
        response = self.client.get(
            "?add_object=Name1&section=objects&add_tariff=1500")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list(obj for obj in Object.objects.all()))
                          , 2)

    def test_remove_object(self):
        self.client.get(
            "?add_object=Name1&section=objects&add_tariff=1500")
        response = self.client.get("?remove_object=2&section=objects")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list(obj for obj in Employee.objects.filter(
            deleted=False))), 1)

    def test_note(self):
        response = self.client.post("", {"tg_idx": 1111,
                                         "names": self.name.id,
                                         "object": self.obj.id,
                                         "pit_number": 1,
                                         "pit_depth": 1,
                                         "pitsize": 2,
                                         })
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(list(note for note in Note.objects.filter(
            deleted=False))), 1)
        self.client.get("?remove_note=1&section=notes")
        self.assertEquals(len(list(note for note in Note.objects.filter(
            deleted=False))), 0)

    def test_report(self):
        self.client._login(self.user)
        self.client.post("", {"tg_idx": 1111,
                              "names": self.name.id,
                              "object": self.obj.id,
                              "pit_number": 1,
                              "pit_depth": 1,
                              "pitsize": 2,
                              })
        response = self.client.post("", {"from": datetime.now().date,
                                         "to": datetime.now().date})
        self.assertEqual(response.status_code, 200)
