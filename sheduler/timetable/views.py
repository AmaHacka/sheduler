from django.views import generic

from .models import Worker, Day
from django.db.models import Q


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        context['workers_list'] = Worker.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
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
        return context

    def construct_hours(self, days, hour_attr):
        days_templte = []
        for day in days:
            t_day = TemplateDay(day.weekday)
            if t_day not in days_templte:
                if day.odd:
                    t_day.odd = getattr(day, hour_attr)
                else:
                    t_day.even = getattr(day, hour_attr)
                days_templte.append(t_day)
            else:
                for d in days_templte:
                    if d == t_day:
                        d.split = True
                        if day.odd:
                            d.odd = getattr(day, hour_attr)
                        else:
                            d.even = getattr(day, hour_attr)
        return map(lambda x: str(x), days_templte)


