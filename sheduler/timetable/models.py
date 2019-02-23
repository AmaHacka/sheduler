from django.db import models

WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
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
        unique=True
    )

    _8_9 = models.BooleanField(default=False, verbose_name="8-9")
    _9_10 = models.BooleanField(default=False, verbose_name="9-10")
    _10_11 = models.BooleanField(default=False, verbose_name="10-11")
    _11_12 = models.BooleanField(default=False, verbose_name="11-12")
    _12_13 = models.BooleanField(default=False, verbose_name="12-13")
    _13_14 = models.BooleanField(default=False, verbose_name="13-14")
    _14_15 = models.BooleanField(default=False, verbose_name="14-15")
    _15_16 = models.BooleanField(default=False, verbose_name="15-16")
    _16_17 = models.BooleanField(default=False, verbose_name="16-17")
    _17_18 = models.BooleanField(default=False, verbose_name="17-18")
    _19_20 = models.BooleanField(default=False, verbose_name="19-20")
    _20_21 = models.BooleanField(default=False, verbose_name="20-21")

    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
