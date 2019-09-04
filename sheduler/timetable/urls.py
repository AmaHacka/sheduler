from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('department/<int:pk>/', views.DepartmentView.as_view(), name='department'),
    path('worker/<int:pk>/', views.WorkerView.as_view(), name='worker'),
    path('worker/<int:pk>/holiday/', views.WorkerHolidayView.as_view(), name='holidays')
]