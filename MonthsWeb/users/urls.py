from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('change_user_password', views.change_user_password, name='change_user_password'),
    path('change_user_details', views.change_user_details, name='change_user_details')
]
