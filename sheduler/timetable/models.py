from django.db import models

WEEKDAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
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

    _8_9 = models.BooleanField(default=False)
    _9_10 = models.BooleanField(default=False)
    _10_11 = models.BooleanField(default=False)
    _11_12 = models.BooleanField(default=False)
    _12_13 = models.BooleanField(default=False)
    _13_14 = models.BooleanField(default=False)
    _14_15 = models.BooleanField(default=False)
    _15_16 = models.BooleanField(default=False)
    _16_17 = models.BooleanField(default=False)
    _17_18 = models.BooleanField(default=False)
    _19_20 = models.BooleanField(default=False)
    _20_21 = models.BooleanField(default=False)

    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
