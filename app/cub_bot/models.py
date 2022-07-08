from django.db import models


class Object(models.Model):
    """ Модель объекта """

    name = models.CharField(max_length=250, blank=False, null=False)
    tariff = models.IntegerField(blank=False, null=False, default=1500)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """ Модель работника """

    name = models.CharField(max_length=250, blank=False, null=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Note(models.Model):
    """ Модель записи """

    tg_idx = models.IntegerField()
    crated_at = models.DateField(auto_now=True)
    names = models.ManyToManyField(Employee, related_name="names")
    obj = models.ForeignKey(Object, related_name="notes",
                            on_delete=models.CASCADE)
    pit_number = models.IntegerField()
    pit_depth = models.FloatField()
    pit_size = models.IntegerField(null=True)
    price = models.FloatField(default=1500)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pit_number} | {self.obj}"
