import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
from .services.dbservice import DatabaseHandler 
from .services.dateservice import DatesHandler
from .services.taskservice import TaskHandler


task_service = TaskHandler(db_service=DatabaseHandler)


def index(request):
    return render(request, 'taskmanager/index.html')


def change_date(request):
	date = request.GET['date']
	
	dates_objects = DatesHandler.generate_month_dates(date, as_objects=True)
	dates_strings = [dt.isoformat() for dt in dates_objects]
	task_dicts = task_service.generate_tasklist_for_dates(dates_objects)
	
	change_month_pack = {
		'dates': dates_strings,
		'tasks': task_dicts 
	}
	
	return JsonResponse(change_month_pack)


def tasks(request):
	if request.method == 'POST':
		task_dict = json.loads(request.body)
		DatabaseHandler.create_task_and_related(task_dict)
		return HttpResponse(status=201)
	else:
		return HttpResponse(status=405)


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
			task_dict = json.loads(request.body)
			DatabaseHandler.update_task_and_related(task_dict)
		return HttpResponse(status=201)

	else:
		return HttpResponse(status=405)