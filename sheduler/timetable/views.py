import datetime
from typing import List, Iterator, Tuple
from collections import OrderedDict

import pytz
from django.db.models import Q
from django.views import generic

from .models import Worker, Day

WEEKDAYS = {
    0: "Пн",
    1: "Вт",
    2: "Ср",
    3: "Чт",
    4: "Пт",
    5: "Сб",
    6: "Вск",
}

DISPLAY_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
TIMEZONE = "Europe/Moscow"
MAXIMUM_HOUR = 21
WEEKDAYS_OFFSET = 1


def get_pretty_date() -> str:
    now = datetime.datetime.now(pytz.timezone(TIMEZONE))
    return f'{now.strftime("%d.%m.%Y")} {WEEKDAYS[now.weekday()]} ({get_weektype()})'


def get_weektype() -> str:
    now_week = datetime.datetime.now().isocalendar()[1]
    if now_week % 2:
        return "Нечетная"
    else:
        return "Четная"


class TemplateDay:
    def __init__(self, name):
        self.name = name
        self.odd = None
        self.even = None
        self.split = False

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        if self.split:
            if self.odd and self.even:
                return "+"
            if self.odd:
                return "+/-"
            if self.even:
                return "-/+"

        else:
            if self.odd or self.even:
                return "+"
        return " "

    def __repr__(self):
        return f"<TemplateDay object {self.name} odd: {self.odd}" \
               f" even: {self.even}> split: {self.split}"


class IndexView(generic.TemplateView):
    template_name = "timetable/index.html"
    timezone = pytz.timezone(TIMEZONE)

    def check_worker_online(self, worker: Worker) -> bool:
        now_time = datetime.datetime.now(self.timezone)
        now_weekday = now_time.weekday() + WEEKDAYS_OFFSET
        now_week = now_time.isocalendar()[1] % 2
        now_hour = now_time.hour
        check_days = Worker.objects.get(pk=worker.pk).day_set.filter(
            weekday=now_weekday)
        if len(check_days) >= 2:
            check_days = list(
                filter(lambda x: getattr(x, "odd") == now_week, check_days))
        now_day = check_days[0]

        if now_hour >= MAXIMUM_HOUR:
            return False
        return getattr(now_day, f"h{now_hour}_{now_hour + 1}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        workers = Worker.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q)).order_by(
            "last_name")

        context["date"] = get_pretty_date()
        context['workers_list'] = [(worker, self.check_worker_online(worker))
                                   for worker in workers]
        return context


class WorkerView(generic.TemplateView):
    template_name = "timetable/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = Worker.objects.get(pk=self.kwargs['pk'])
        context['object'] = worker
        days = worker.day_set.all()
        hours = [a for a in Day.__dict__.keys() if a.startswith("h")]
        # В стоках - часы работы, в столбцах - дни
        # Day._meta.get_field(h).verbose_name - взять атрибут verbose_name
        table = {
            Day._meta.get_field(h).verbose_name: self.construct_hours(days, h)
            for h
            in hours}
        context["table"] = table
        context["display_days"] = DISPLAY_DAYS
        context["date"] = get_pretty_date()
        sum_hours = self.sum_hours(days)
        context["hours_sum"] = sum_hours
        context["hours_average"] = (sum_hours[0] + sum_hours[1]) / 2
        return context

    @staticmethod
    def construct_hours(days: List[Day], hour_attr: str) -> Iterator[str]:
        days_templte = []
        days = list(days)
        days.sort(key=lambda x: x.weekday)
        for day in days:
            t_day = TemplateDay(day.weekday)
            if t_day not in days_templte:
                t_day.split = day.split
                if day.odd:
                    t_day.odd = getattr(day, hour_attr)
                else:
                    t_day.even = getattr(day, hour_attr)
                days_templte.append(t_day)
            else:
                for d in days_templte:
                    if d == t_day:
                        # d.split = True
                        if day.odd:
                            d.odd = getattr(day, hour_attr)
                        else:
                            d.even = getattr(day, hour_attr)
        return map(lambda x: str(x), days_templte)

    @staticmethod
    def sum_hours(days: List[Day]) -> Tuple[int, int]:
        odd_sum = 0
        even_sum = 0
        for day in days:
            hours = [value for key, value in day.__dict__.items() if
                     key.startswith("h")]
            for hour in hours:
                if day.split:
                    if day.odd and hour:
                        odd_sum += 1
                    elif not day.odd and hour:
                        even_sum += 1
                elif hour:
                    odd_sum += 1
                    even_sum += 1
        return odd_sum, even_sum


class WorkerHolidayView(generic.TemplateView):
    template_name = "timetable/holiday_detail.html"
    holidays_count = 28
    now = datetime.datetime.now()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        holidays = Worker.objects.get(pk=self.kwargs['pk']).holiday_set.all()
        this_year_holidays = filter(self.filter_year, holidays)
        context["holidays"] = list(
            map(self.construct_holiday, this_year_holidays))
        left_free_days = self.holidays_count
        for holiday in context["holidays"]:
            left_free_days -= holiday[0]
        context["days_left"] = left_free_days
        return context

    @staticmethod
    def construct_holiday(holiday):
        delta_holiday = holiday.date_end - holiday.date_start
        length = delta_holiday.days + 1
        return length, holiday

    def filter_year(self, holiday):
        if self.now.year == holiday.date_start.year:
            return True
        else:
            return False
