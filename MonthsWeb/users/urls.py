from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
     # registration
     path(route='register',
          view=views.UserRegistration.as_view(),
          name='register'),
     # user settings and details
     path(route='user_settings/',
          view=views.UserSettings.as_view(),
          name='user_settings'),
     path(route='change_user_password',
          view=views.UserPasswordChanging.as_view(),
          name='change_user_password'),
     path(route='change_user_details',
          view=views.UserDetailsChanging.as_view(),
          name='change_user_details'),
     # user password reset
     path(route='password_reset/',
          view=views.ResetUserPassword.as_view(),
          name='password_reset'),
     path(route='password_reset/done',
          view=auth_views.PasswordResetDoneView.as_view(),
          name='password_reset_done'),
     path(route='reset/<uidb64>/<token>',
          view=auth_views.PasswordResetConfirmView.as_view(),
          name='password_reset_confirm'),
     path(route='password_reset_complete',
          view=auth_views.PasswordResetCompleteView.as_view(),
          name='password_reset_complete')    
]
