from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class UserDetailsChangingForm(forms.ModelForm):
    """Change username, useremail, etc. (except the password)."""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)



class RegisterForm(UserCreationForm):
    email = forms.EmailField()