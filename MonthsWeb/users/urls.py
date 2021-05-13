from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('user_settings/', views.user_settings, name='user_settings'),
]
