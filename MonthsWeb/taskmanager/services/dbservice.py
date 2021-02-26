from datetime import datetime
from typing import Iterable, overload
from django.db.models import query, CharField
from django.db.models.fields import AutoField, related_descriptors
from django.db.models.functions import Cast
from django.utils import timezone
from .. import models


class Database_handler:

    @staticmethod
    def get_monthly_tasks(dates_period:tuple):
        """Takes a tuple of two datetime objects and retrieves from database
        all the tasks (all fields including fields from related tables), that
        matches this time period (except the fields, which can be multiple for 
        each task.ID: "completion" and "file")
        """
        values_list = models.Task.objects\
            .values_list('id', 
                         Cast('init_date', output_field=CharField()), 
                         'title', 
                         'description',
                         'interval',
                         'autoshift')\
            .filter(init_date__range=dates_period)
        
        return values_list
    
    @staticmethod
    def get_intervalled_tasks(dates_period:tuple):
        """ Takes a tuple of two datetime objects, where the first is the
        beginning- and the second is the end- of the time period. The method
        finds all interval-based tasks that matches the period and returns a
        list of tuples. The first element of each tuple is interval-string
        (e.g. "every_day", "every_month" etc.) and remaining elements are
        fields of the task such as: ID, date of the task's creation, title,
        task, description.
        """
        _, date_until = dates_period  # needs only end-date of period
        
        values_list = models.Task.objects\
            .values_list('interval',
                         'id',
                          Cast('init_date', output_field=CharField()),  # as a string
                         'title', 
                         'description',
                         'autoshift')\
            .filter(init_date__lt=date_until)\
            .exclude(interval='no')
        
        return values_list

    @staticmethod
    def get_additional_fields(task_IDs_list:list):
        """ Takes a list of task IDs and extracts data from tables that
        contains additional information about each task with the given ID.
        Returns a list of tuples containing the task's ID, task's completion
        date, and files associated with the task.
        """
        query_set = models.Task.objects\
            .select_related('completion', 'file')\
            .values_list(     
                'id',                              # as a string ↴
                Cast('completion__date_completed', output_field=CharField()), 
                'file__id',
                'file__link',
                'file__related_task_id')\
            .filter(id__in=task_IDs_list)
        
        return list(query_set)
    
    @staticmethod
    def add_overall_task(overall_dict):
        """Takes a dict of all fields of the task (arg "overall_dict") 
        and inserts them into related sql tables.
        """
        # isostring to datetime object
        task_creation_time = timezone.datetime.fromisoformat(
                                                    overall_dict['init_date'])

        if overall_dict['autoshift'] == 'no':
            overall_dict['autoshift'] = False
        elif overall_dict['autoshift'] == 'yes':
            overall_dict['autoshift'] = True

        models.Task.objects.create(init_date=task_creation_time,
                                   title=overall_dict['title'],
                                   description=overall_dict['description'],
                                   interval=overall_dict['interval'],
                                   autoshift=overall_dict['autoshift'])
        # TODO: adding in db attached files

    @staticmethod
    def update_overall_task(overall_dict):
        """ Takes a dict of all fields of the task and adds them into
        related sql tables.
        """
        # Check input
        required_keys = ['ID', 'initdate', 'title', 'description',
                         'interval', 'autoshift']
        if not all(k in overall_dict.keys() for k in required_keys):
            raise KeyError('failed to update the Task, missing one ',
                          f'or more of the required keys: {required_keys}')
        
        # Prepare some fields
        task_id = overall_dict['ID']
        initdate_object = timezone.datetime\
            .fromisoformat(overall_dict['initdate'])  # ISOstring to datetime
        
        # Updating tables
        models.Task.objects.filter(pk=task_id)\
            .update_or_create(initdate=initdate_object,
                   title=overall_dict['title'],
                   description=overall_dict['description'])
        
        if 'interval' in overall_dict.keys():
            models.Interval.objects.filter(related_task_id=task_id)\
                .update(interval=overall_dict['interval'])
        
        if 'autoshift' in overall_dict.keys():
            models.Autoshift.objects.filter(related_task_id=task_id)\
                .update(autoshift=overall_dict['autoshift'])
        
    @staticmethod
    def delete_task(task):
        """ Delete task by id from core table 'task' and other tables related
        via foreign key. As an argument can be provided a dict, that contains
        {'ID': id_integer} key: value pair or direct integer ID value
        """
        if isinstance(task, dict):
            task_id = task['ID']
        elif isinstance(task, int):
            task_id = task
        else:
            raise ValueError('the argument must be type of dict or int')

        models.Task.objects.filter(ID=task_id).delete()

    def check_uncheck_task(self):
        pass

    def shift_tasks(self):
        pass
