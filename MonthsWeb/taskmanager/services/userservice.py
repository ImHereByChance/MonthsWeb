from django.contrib.auth.models import User
from ..models import UserProfile


def set_user_profile(user: User, **kwargs: dict) -> None:
    """Set the values of the UserProfile fields (of the model related to
    the user). The first positional argument must be a User object,
    the rest must be keyword arguments, which are UserProfile fields. 
    """
    
    try:
        user.userprofile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=user)

    for key, value in kwargs.items():
        if hasattr(user.userprofile, key):
            setattr(user.userprofile, key, value)
        else:
            raise KeyError(f'invalid property given: {key}')
