from django.contrib import admin

# Register your models here.
from .models import Worker, Day


class DayInline(admin.TabularInline):
    model = Day

    def get_extra(self, request, obj=None, **kwargs):
        extra = 5
        if obj:
            return 0
        return extra


class WorkerAdmin(admin.ModelAdmin):
    inlines = [DayInline]


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Day)
