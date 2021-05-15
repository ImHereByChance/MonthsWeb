from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.views import View
from django.utils.decorators import method_decorator

from .forms import RegisterForm, UserDetailsChangingForm
from .services.misc import dispatch_messages


class UserRegistration(View):
    """ Page to get the registration form or submit it."""
    form_class = RegisterForm
    tamplate = 'registration/register.html'

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.tamplate, context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')


class UserDetailsChanging(View):
    """ A view to handle the form that in charge of changing the
    fields of the User model (excluding password).
    """

    form_class = UserDetailsChangingForm

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(data=request.POST,
                               instance=request.user)
        if form.is_valid():
            messages.success(request=request,
                             message='changes saved',
                             extra_tags='user_details_form')
            form.save()
        else:
            for field_name, error_list in form.errors.items():
                for err_msg in error_list:
                    messages.error(request=request,
                                   message=err_msg,
                                   extra_tags=field_name)

        return redirect('user_settings')


class ChangingUserPassword(View):
    """ A view for processing the form that in charge of changing user
    passwords (by entering the old and new passwords).
    """
    form_class = PasswordChangeForm

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(data=request.POST, user=request.user)

        if form.is_valid():
            messages.success(request=request,
                             message='Successfully Changed',
                             extra_tags='password_change_form')
            form.save()

            username = request.user.username
            password = form.cleaned_data['new_password1']
            user = authenticate(username=username, password=password)
            login(request, user)

        else:
            for field_name, error_list in form.errors.items():
                for err_msg in error_list:
                    messages.error(request=request,
                                   message=err_msg,
                                   extra_tags=field_name)

        return redirect('user_settings')


class UserSettings(View):
    """ A View to handle the page where users change their preferences
    and details. The page contains multiple forms, each with their own 
    submit-inputs and views to processing a POST request (the current
    view only renders the page with thouse forms - not processing them)
    """

    template_name = 'registration/user_settings.html'

    @method_decorator(login_required)
    def get(self, request):
        user_details_form = UserDetailsChangingForm(instance=request.user)
        password_change_form = PasswordChangeForm(user=request.user)

        context = {
            'user': request.user,
            'user_details_form': user_details_form,
            'password_change_form': password_change_form
        }

        message_storage = messages.api.get_messages(request)
        if message_storage:
            messages_dict = dispatch_messages(message_storage)
            context.update(messages_dict)

        return render(request, self.template_name, context)
