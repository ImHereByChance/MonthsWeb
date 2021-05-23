from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views import View
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


class UserSettingsFormHandler(View):
    """ A view to handle one of the forms (located on user-settings
    page) that in charge of changing the fields of the User or
    UserProfile models.
    """
    form_class = None
    form_name = None
    redirect_view_name = None
    success_message = None

    @method_decorator(login_required)
    def post(self, request, *form_args, **form_kwargs):
        form = self.form_class(*form_args, **form_kwargs)
        if form.is_valid():
            self.on_success(request, form)
        else:
            self.on_failure(request, form)  
        return redirect(self.redirect_view_name)
    
    def on_success(self, request, form):
        """ Will be called if submitted `form.is_valid()`"""
        # Make a massage about successfull processing of the form using
        # django.contrib.messages
        if self.success_message:
            messages.success(request=request,
                            message=self.success_message,
                            extra_tags=self.form_name)      
        form.save()

    def on_failure(self, request, form):
        """ Will be called if not`form.is_valid()`"""
        # make `django.contrib.messages` for each of form.errors
        self.make_error_messages(request, form)

    def make_error_messages(self, request, form):
        """ Make `django.contrib.messages` for each of form.errors"""
        for field_name, error_list in form.errors.items():
            for err_msg in error_list:
                messages.error(request=request,
                               message=err_msg,
                               extra_tags=field_name)
