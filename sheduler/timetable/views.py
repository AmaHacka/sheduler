from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader

from .models import Worker


def index(request):
    workers = Worker.objects.all()
    template = loader.get_template('timetable/index.html')
    context = {
        'workers_list': workers,
    }
    return HttpResponse(template.render(context, request))


def worker(request, user_id):
    return HttpResponse("Here detailed user view")
