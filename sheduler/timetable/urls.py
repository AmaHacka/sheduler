from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('parts/', views.sync_time),
    path('<int:pk>/', views.WorkerView.as_view(), name='worker'),
    path('<int:pk>/holiday/', views.WorkerHolidayView.as_view(), name='holidays')
]