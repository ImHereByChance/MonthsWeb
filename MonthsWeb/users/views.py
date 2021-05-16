from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _

from .forms import RegisterForm, UserDetailsChangingForm
from .services.misc import dispatch_messages
from .view_classes import UserSettingsPageForm 


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


class UserDetailsChanging(UserSettingsPageForm):
    """ A view to handle the form that in charge of changing the
    fields of the User model (excluding password).
    """
    form_class = UserDetailsChangingForm
    form_name = 'user_details_form'
    redirect_view_name = 'user_settings'
    success_message = _('changes saved')

    @method_decorator(login_required)
    def post(self, request):
        return super().post(request, data=request.POST, instance=request.user)


class UserPasswordChanging(UserSettingsPageForm):
    """ A view for processing the form that in charge of changing user
    passwords (by entering the old and new passwords).
    """
    form_class = PasswordChangeForm
    form_name = 'password_change_form'
    redirect_view_name = 'user_settings'
    success_message = _('password successfully saved')

    def post(self, request):
        return super().post(request, data=request.POST, user=request.user)
    
    def on_success(self, request, form):
        super().on_success(request, form)
        username = request.user.username
        password = form.cleaned_data['new_password1']
        user = authenticate(username=username, password=password)
        login(request, user)


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
