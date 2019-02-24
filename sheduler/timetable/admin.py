from django.contrib import admin

# Register your models here.
from .models import Worker, Day


class DayInline(admin.TabularInline):
    model = Day
    extra = 5


class WorkerAdmin(admin.ModelAdmin):
    inlines = [DayInline]


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Day)
