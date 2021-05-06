from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """A model for storing user preferences."""

    # standard Django User model as foreign key
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False) 
    # the language of the user interface
    language = models.CharField(max_length=20, blank=True)