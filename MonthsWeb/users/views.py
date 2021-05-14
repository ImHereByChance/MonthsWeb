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
def change_user_details(request):
    """ A view to handle the form that in charge of changing the
    fields of the User model (excluding password).
    """
    
    if request.method != 'POST':
            return HttpResponse(status=405)

    form = UserDetailsChangingForm(data=request.POST,
                                   instance=request.user)
    
    if form.is_valid():
        messages.success(request=request,
                         message='Successfully Changed',
                         extra_tags='user_details_form')
        form.save()
    
    else:
        for field_name, error_list in form.errors.items():
                    for err_msg in error_list:
                        messages.error(request=request,
                                       message=err_msg,
                                       extra_tags=field_name)

    return redirect('user_settings')
   
    

@login_required
def change_user_password(request):
    """ A view for processing the form that in charge of changing user
    passwords (by entering the old and new passwords).
    """

    if request.method != 'POST':
        return HttpResponse(status=405)
    
    form = PasswordChangeForm(data=request.POST, user=request.user)

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
        
         
    

@login_required
def user_settings(request):
    """ A View to handle the page where users change their preferences
    and details. The page contains multiple forms, each with their own 
    submit-inputs and views to processing POST request (current view
    only renders the page with thouse forms - not processing them).
    """
    
    if not request.method == 'GET':
        return HttpResponse(status=405)

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
