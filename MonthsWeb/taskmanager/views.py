from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .services.dbservice import Database_handler 


def index(request):
    return render(request, 'taskmanager/index.html')

def test_target(request):
    """tmp vie for testing perposes"""
    
    dct = {'date': '2021-01-12 00:00:00', 'ID': 78, 
        'initdate': '2021-01-12 00:00:00', 'title': 'sf', 
        'description': 'fsf', 'interval': 'no', 'autoshift': 'no', 
        'completion': False, 'files': []}
    Database_handler.add_overall_task(dct)
    return HttpResponse('vse')