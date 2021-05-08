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
    """TODO: fill this docstring"""
    if request.method == 'POST':
        form = UserDetailsChangingForm(request.POST, instance=request.user)
        
        context = {
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
    """ TODO: fill this docstring"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        context = {
            'user_details_form': form,
            'password_change_form': PasswordChangeForm(request.user),
        }

        if form.is_valid():
            form.save()
            username = request.user.username
            password = form.cleaned_data['new_password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            context['password_changed_msg'] = 'password changed'

        return redirect(reverse('user_settings'), kwargs=context)

    else:
        return HttpResponse(status=405)
    

@login_required
def user_settings(request):
    """TODO: fill this docstring"""
    
    user_details_form = UserDetailsChangingForm(instance=request.user)
    password_change_form = PasswordChangeForm(request.user)
    
    
    context = {
        'password_change_form': password_change_form,
        'user_details_form': user_details_form,
    }

    return render(request, 'registration/user_settings.html', context)

