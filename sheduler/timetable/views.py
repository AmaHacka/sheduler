from django.views import generic

from .models import Worker, Day
from django.db.models import Q


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
        table = {Day._meta.get_field(h).verbose_name: [getattr(d, h) for d in days] for h in hours}
        context["table"] = table
        return context
