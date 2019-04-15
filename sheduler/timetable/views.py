import datetime
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


def get_pretty_date():
    now = datetime.datetime.now(pytz.timezone(TIMEZONE))
    return f'{now.strftime("%d.%m.%Y")} {WEEKDAYS[now.weekday()]} ({get_weektype()})'


def get_weektype():
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
        return f"<TemplateDay object {self.name} odd: {self.odd} even: {self.even}> split: {self.split}"


class IndexView(generic.TemplateView):
    template_name = "timetable/index.html"
    timezone = pytz.timezone(TIMEZONE)

    def check_worker_online(self, worker):
        now_time = datetime.datetime.now(self.timezone)
        now_weekday = now_time.weekday() + WEEKDAYS_OFFSET
        now_week = now_time.isocalendar()[1] % 2
        now_hour = now_time.hour
        check_days = Worker.objects.get(pk=worker.pk).day_set.filter(weekday=now_weekday)
        if len(check_days) >= 2:
            check_days = list(filter(lambda x: getattr(x, "odd") == now_week, check_days))
        now_day = check_days[0]

        if now_hour >= MAXIMUM_HOUR:
            return False
        return getattr(now_day, f"h{now_hour}_{now_hour + 1}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        workers = Worker.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q)).order_by("last_name")

        context["date"] = get_pretty_date()
        context['workers_list'] = [(worker, self.check_worker_online(worker)) for worker in workers]
        return context


class WorkerView(generic.TemplateView):
    template_name = "timetable/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Worker.objects.get(pk=self.kwargs['pk'])
        days = Worker.objects.get(pk=self.kwargs['pk']).day_set.all()
        hours = [a for a in Day.__dict__.keys() if a.startswith("h")]
        # В стоках - часы работы, в столбцах - дни
        # Day._meta.get_field(h).verbose_name - взять атрибут verbose_name
        table = {Day._meta.get_field(h).verbose_name: self.construct_hours(days, h) for h in hours}
        context["table"] = table
        context["display_days"] = DISPLAY_DAYS
        context["date"] = get_pretty_date()
        return context

    def construct_hours(self, days, hour_attr):
        days_templte = []
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
