from django.urls import path
from . import views


urlpatterns = [
    path(route='register',
         view=views.UserRegistration.as_view(),
         name='register'),
    path(route='user_settings/',
         view=views.UserSettings.as_view(),
         name='user_settings'),
    path(route='change_user_password',
         view=views.ChangingUserPassword.as_view(),
         name='change_user_password'),
    path(route='change_user_details',
         view=views.UserDetailsChanging.as_view(),
         name='change_user_details')
]
