from django.contrib import admin

# Register your models here.
from .models import Worker, Day, Holiday


class DayInline(admin.TabularInline):
    model = Day

    def get_extra(self, request, obj=None, **kwargs):
        extra = 5
        if obj:
            return 0
        return extra


class HolidayInline(admin.StackedInline):
    model = Holiday

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra


class WorkerAdmin(admin.ModelAdmin):
    inlines = [DayInline, HolidayInline]


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Day)
