from datetime import datetime
from django.db.models import query, CharField
from django.db.models.fields import related_descriptors
from django.db.models.functions import Cast
from django.utils import timezone
from .. import models


class Database_handler:

    @staticmethod
    def get_monthly_tasks(dates_period):
        """Takes a tuple of two datetime objects and retrieves from database 
        all the tasks (all fields including fields from related tables), that 
        matches this time period (except the fields, which can be multiple for
        each task.ID: "completion" and "file")
        """
        query_set = models.Task.objects\
            .select_related('interval', 'autoshift')\
            .values_list(  
                # retrieves 'initdate' as a string
                'ID', Cast('initdate', output_field=CharField()),
                'title','description', 
                'autoshift__value', 'interval__interval')\
            .filter(initdate__range=dates_period)
        return list(query_set)
    
    @staticmethod
    def get_intervalled_tasks(dates_period):
        """ Takes a tuple of two datetime objects, where the first is the 
        beginning- and the second is the end- of the time period. The method 
        finds all interval-based tasks that matches the period and returns a 
        list of tuples. The first element of each tuple is interval-string 
        (e.g. "every_day", "every_month" etc.) and remaining elements are 
        fields of the task such as: ID, date of the task's creation, title,
        task, description.
        """
        _, date_until = dates_period  # needs only the "date until"
        
        query_set = models.Task.objects\
            .select_related('interval')\
            .values_list(
                'interval__interval', 'ID', 'title',
                # retrieves 'initdate' as a string
                Cast('initdate', output_field=CharField()), 
                'description')\
            .filter(interval__isnull=False, initdate__lt=date_until)\
            .exclude(interval__interval='no')
        
        return list(query_set)

    @staticmethod
    def get_additional_fields(task_IDs_list):
        """ Takes a list of task IDs and extracts data from tables that 
        contains additional information about each task with the given ID.
            Returns a list of tuples containing the task's ID, task's 
        completion date, and files associated with the task.
        """
        # TODO: fix multiple files for single task situation 
        query_set = models.Task.objects\
            .select_related('completion', 'file')\
            .values_list(
                # retrieves 'completion__date_when' as a string
                'ID', Cast('completion__date_when', 
                            output_field=CharField()), 
                'file__ID', 'file__link', 'file__related_task_id')\
            .filter(ID__in=task_IDs_list)
        
        return str(query_set)
    
    @classmethod
    def add_overall_task(cls, overall_dict):
        """Takes a dict of all fields of the task (arg "overall_dict") 
        and inserts them into related sql tables.
        """
        required_keys = ['initdate', 'title', 'description',
                         'interval', 'autoshift']
        if not all(k in overall_dict.keys() for k in required_keys):
            raise KeyError('failed to add the task to database, missing one ',
                          f'or more of the required keys: {required_keys}')

        task_creation_time = timezone.datetime.\
                                fromisoformat(overall_dict['initdate'])

        new_task = models.Task.objects.create(
            initdate=task_creation_time,
            title=overall_dict['title'],
            description=overall_dict['description']
        )
        models.Interval.objects.create(
                interval=overall_dict['interval'],
                related_task=new_task   
            )
        models.Autoshift.objects.create(
                value=overall_dict['autoshift'],
                related_task=new_task
            )
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
