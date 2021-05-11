from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegisterForm, UserDetailsChangingForm


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
def change_user_details(request):
    """ A view to handle the form that in charge of changing the
    fields of the User model (excluding password).
    """
    if request.method == 'POST':
        form = UserDetailsChangingForm(request.POST, instance=request.user)
        
        context = {
            'user': request.user.user,
            'user_details_form': form,
            'password_change_form': PasswordChangeForm(request.user),
        }

        if form.is_valid():
            form.save()
            context['user_detail_canged_msg'] = 'changes saved'
        
        return render(request, 'registration/user_settings.html', context)
            
    else:
        return HttpResponse(status=405)
    

@login_required
def change_password(request):
    """ A view to handle the form for userpasswords changing. """

    if request.method == 'POST':
        password_canged_form = PasswordChangeForm(request.user,
                                                  request.POST)
        context = {
            'user': request.user,
            'user_details_form': UserDetailsChangingForm(instance=request.user),
            'password_change_form': password_canged_form,
        }

        if password_canged_form.is_valid():
            password_canged_form.save()
            username = request.user.username
            password = password_canged_form.cleaned_data['new_password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            context['password_changed_msg'] = 'password changed'
        
        return render(request, 'registration/user_settings.html', context)

    else:
        return HttpResponse(status=405)
    

@login_required
def user_settings(request):
    """ The view that returns the page with usersettings. Settings are
    made up of individual forms that are handled by their own views
    (current view only renders the page with thouse forms - not handles
    them, hence the only allowed method is get).
    """
    
    if not request.method == 'GET':
        return HttpResponse(status=405)

    user_details_form = UserDetailsChangingForm(instance=request.user)
    password_change_form = PasswordChangeForm(request.user)
    
    context = {
        'user': request.user,
        'password_change_form': password_change_form,
        'user_details_form': user_details_form,
    }

    return render(request, 'registration/user_settings.html', context)



