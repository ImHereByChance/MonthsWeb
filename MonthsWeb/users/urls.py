from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('user_details_change/', views.change_user_details, name='user_details_change'),
    path('password_change/', views.change_password, name='password_change'),
]
