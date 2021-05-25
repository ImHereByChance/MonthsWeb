import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils.translation import get_language

from .models import Task
from .services.dbservice import DatabaseHandler
from .services.dateservice import DatesHandler
from .services.taskservice import TaskHandler


task_service = TaskHandler(db_service=DatabaseHandler)


@login_required
def index(request):
    """ Index page and also the entry point for the js app. """
    
    context = {'user': request.user}
    return render(request, 'taskmanager/index.html', context)


@login_required
def change_date(request):
    """ Returns json with tasks and dates (as isoformat strings) for the
    date given in the get-request parameter. E.g.:
    "getDatePack/?date=2021-06-01T00%3A00%3A00.000%2B00%3A00"
    """
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
    """ Endpoint for creating a task in the database. New task fields
    should be submitted via post request as json object. 
    """
    if request.method == 'POST':
        task_dict = json.loads(request.body)
        DatabaseHandler.create_task_and_related(task_dict, request.user)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=405)


@login_required
def tasks_by_id(request, task_id):
    """ Endpoint for getting, deleting and updating a task in database.
    e.i: tasks/<int:task_id>/
    """
    if request.method == 'GET':
        try:
            task = Task.objects.values().get(id=task_id, user=request.user)
            return JsonResponse(task)
        except Task.DoesNotExist:
            return HttpResponse(status=404)

    elif request.method == 'DELETE':
        try:
            DatabaseHandler.delete_task(task_id, user=request.user)
            return HttpResponse(status=200)
        except Task.DoesNotExist:
            return HttpResponse(status=404)

    elif request.method == 'PUT':
        task_dict = json.loads(request.body)
        if 'checkUncheck' in request.headers.keys():
            DatabaseHandler.check_uncheck_task(task_dict)
        else:
            DatabaseHandler.update_task_and_related(task_dict, request.user)
        return HttpResponse(status=201)

    else:
        return HttpResponse(status=405)
