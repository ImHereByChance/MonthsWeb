from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('getDatePack/', views.change_date, name='change_date'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:task_id>/', views.tasks_by_id, name='tasks_by_id'),
    path('register', views.register, name='register'),
]
