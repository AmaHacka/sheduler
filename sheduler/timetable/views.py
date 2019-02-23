from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.
from django.template import loader

from .models import Worker


class IndexView(generic.TemplateView):
    template_name = "timetable/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workers_list'] = Worker.objects.all()
        return context


class WorkerView(generic.DetailView):
    model = Worker
