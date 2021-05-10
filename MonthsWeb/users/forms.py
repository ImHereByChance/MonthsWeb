from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UserDetailsChangingForm(forms.ModelForm):
    """Change username, useremail, etc. (except the password)."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)
        label = {
            'usename': _('User name: '),
            'email': _('Email: '),
            'first_name': _('First name: '),
            'last_name': _('Last name: ')
        }

    def clean_email(self):
        new_email = self.cleaned_data['email']
        if User.objects\
            .filter(email=new_email)\
            .exclude(id=self.instance.id)\
            .exists():
            raise ValidationError(
                _('A user with that email already exists.'),
            )
        return new_email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class RegisterForm(UserCreationForm):
    """ A form to create new Users.
    Extended from django.contrib.auth.forms.UserCreationForm
    """
    
    email = forms.EmailField()

    def clean_email(self):
        new_email = self.cleaned_data['email']
        if User.objects.filter(email=new_email).exists():
            raise ValidationError(
                _('A user with that email already exists.'),
                code='not_unique_email'
            )
        return new_email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
