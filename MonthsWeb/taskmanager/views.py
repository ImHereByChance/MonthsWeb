import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import get_language

from .forms import RegisterForm
from .models import Task
from .services.dbservice import DatabaseHandler
from .services.dateservice import DatesHandler
from .services.taskservice import TaskHandler


task_service = TaskHandler(db_service=DatabaseHandler)


@login_required
def index(request):
    language_code = get_language()
    context = {
        'username': request.user.username,
        'language_code': language_code
    }
    return render(request, 'taskmanager/index.html', context)


def register(request):
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
def change_date(request):
    date = request.GET['date']

    dates_objects = DatesHandler.generate_month_dates(date, as_objects=True)
    dates_strings = [dt.isoformat() for dt in dates_objects]
    task_dicts = task_service.generate_tasklist_for_dates(dates_objects,
                                                          user=request.user)

    change_month_pack = {
        'dates': dates_strings,
        'tasks': task_dicts
    }

    return JsonResponse(change_month_pack)


@login_required
def tasks(request):
    if request.method == 'POST':
        task_dict = json.loads(request.body)
        DatabaseHandler.create_task_and_related(task_dict, request.user)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=405)


@login_required
def tasks_by_id(request, task_id):
    if request.method == 'GET':
        task = Task.objects.values().get(id=task_id)
        return JsonResponse(task)

    elif request.method == 'DELETE':
        DatabaseHandler.delete_task(task_id)
        return HttpResponse(status=200)

    elif request.method == 'PUT':
        task_dict = json.loads(request.body)
        if 'checkUncheck' in request.headers.keys():
            DatabaseHandler.check_uncheck_task(task_dict)
        else:
            DatabaseHandler.update_task_and_related(task_dict)
        return HttpResponse(status=201)

    else:
        return HttpResponse(status=405)
