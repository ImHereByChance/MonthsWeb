from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .services.dbservice import DatabaseHandler 


def index(request):
    return render(request, 'taskmanager/index.html')

def test_target(request):
    """tmp view for testing perposes"""
    
    DatabaseHandler.delete_task(11)
    
    return HttpResponse('success')