from django.contrib.auth.models import User
from django.contrib import messages
from ..models import UserProfile


def dispatch_messages(messages: list) -> dict:
    """ Takes django messages object (list-like) and turns it to a dict
    like that:
    ```
    { "error_messages": { "first_list": ["message1", "message2", ...],
                        "second_list": ["message3", "message4"], 
                        ... },
      "success_messages": { "first_list": ["message1", ... ],
                          ... },
      ...
    ```
    The tag of the message (debug, info, error, etc) and names of the dicts
    with the messages of that level ('debug_messages', 'error_messages,
    etc) been generated automatically. The key-names of the lists nested
    in these "level dicts" been provident by the arg "extra_tags" for
    the messages class. 
    """
    dict_of_dicts = {}

    for msg in messages:
        dict_name = msg.level_tag + '_messages'  # -> e.g. 'error_messages'
        level_dict = dict_of_dicts.get(dict_name)

        if level_dict is None:
            dict_of_dicts.update({dict_name: dict()})
            level_dict = dict_of_dicts.get(dict_name)

        list_name = msg.extra_tags or 'nameless'
        field_list = level_dict.get(list_name)

        if field_list is None:
            level_dict.update({
                list_name: list()
            })

        level_dict.get(list_name).append(msg.message)

    return dict_of_dicts


def set_user_profile(user: User, **kwargs: dict) -> None:
    """Set the values of the UserProfile fields (the model related to
    the User which stores personal settings). The first positional
    argument must be a User object, the rest must be keyword arguments,
    which are `models.UserProfile` fields. 
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
