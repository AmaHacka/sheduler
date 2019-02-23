from django.contrib import admin

# Register your models here.
from .models import Worker, Day

admin.site.register(Worker)
admin.site.register(Day)
