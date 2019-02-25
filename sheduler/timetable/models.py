from django.db import models

WEEKDAYS = [
    (1, "Понедельник"),
    (2, "Вторник"),
    (3, "Среда"),
    (4, "Четверг"),
    (5, "Пятница"),
]


class Worker(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    full_day = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Day(models.Model):
    weekday = models.IntegerField(
        choices=WEEKDAYS,
    )
    odd = models.BooleanField(default=False, verbose_name="Нечетная")

    h8_9 = models.BooleanField(default=False, verbose_name="8-9")
    h9_10 = models.BooleanField(default=False, verbose_name="9-10")
    h10_11 = models.BooleanField(default=True, verbose_name="10-11")
    h11_12 = models.BooleanField(default=True, verbose_name="11-12")
    h12_13 = models.BooleanField(default=True, verbose_name="12-13")
    h13_14 = models.BooleanField(default=True, verbose_name="13-14")
    h14_15 = models.BooleanField(default=True, verbose_name="14-15")
    h15_16 = models.BooleanField(default=True, verbose_name="15-16")
    h16_17 = models.BooleanField(default=True, verbose_name="16-17")
    h17_18 = models.BooleanField(default=True, verbose_name="17-18")
    h18_19 = models.BooleanField(default=False, verbose_name="18-19")
    h19_20 = models.BooleanField(default=False, verbose_name="19-20")
    h20_21 = models.BooleanField(default=False, verbose_name="20-21")

    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
