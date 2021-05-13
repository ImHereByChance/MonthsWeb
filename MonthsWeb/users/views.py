from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RegisterForm, UserDetailsChangingForm
from .services.misc import dispatch_messages


def register(request):
    """ Page to get the registration form or submit it."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def user_settings(request):
    """View to handle the page where users can change their preferences
    and details. The page contains multiple forms which have their own 
    submit-inputs (all of them are being handled here).
    """

    if request.method == 'GET':
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

        return render(request, 'registration/user_settings.html', context)

    elif request.method == 'POST':

        form_name = request.POST.get('form_name')  # <input type="hidden" ...

        if form_name == 'user_details_form':
            user_details_form = UserDetailsChangingForm(data=request.POST,
                                                        instance=request.user)
            password_change_form = PasswordChangeForm(user=request.user)
        elif form_name == 'password_change_form':
            password_change_form = PasswordChangeForm(data=request.POST,
                                                      user=request.user)
            user_details_form = UserDetailsChangingForm(instance=request.user)
        else:
            raise Exception('Cannot define which form was submitted')

        context = {
            'user': request.user,
            'user_details_form': user_details_form,
            'password_change_form': password_change_form,
            'submitted_form': form_name
        }

        for form in (user_details_form, password_change_form):
            if form.is_bound:
                if not form.is_valid():
                    for field_name, error_list in form.errors.items():
                        for err_msg in error_list:
                            messages.error(request=request,
                                           message=err_msg,
                                           extra_tags=field_name)
                    return redirect('user_settings')

                elif form_name == 'user_details_form':
                    messages.success(request=request,
                                     message='Successfully Changed',
                                     extra_tags='user_details_form')
                    form.save()

                elif form_name == 'password_change_form':
                    messages.success(request=request,
                                     message='Successfully Changed',
                                     extra_tags='password_change_form')
                    form.save()

                    username = request.user.username
                    password = form.cleaned_data['new_password1']
                    user = authenticate(username=username, password=password)
                    login(request, user)

        return redirect('user_settings')

    else:
        return HttpResponse(status=405)
