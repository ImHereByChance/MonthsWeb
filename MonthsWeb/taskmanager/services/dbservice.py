from django.db.models import query
from django.db.models.fields import related_descriptors
from .. import models


class Database_handler:
    @staticmethod
    def get_monthly_tasks(dates_period):
        """Takes a tuple of two dates and retrieves from database all fields of
        the tasks, that matches this period (except the fields, which can be 
        multiple for each task.ID: "completion" and "file")"""
        
        query_set = models.Task.objects\
            .select_related('interval', 'autoshift')\
            .values_list('ID', 'initdate', 'title',\
                         'description', 'autoshift__value',\
                         'interval__interval')\
            .filter(initdate__range=dates_period)
        return list(query_set)
    
    @staticmethod
    def get_intervalled_tasks(dates_period):
        """ Takes tuple containing start- and end- date strings of the chosen
        time period which are formatted as YYYY-MM-DD HH:HH:SS. Finds all tasks
        with intervals that match given range of dates and returns a list of
        tuples where in each tuple the first element is interval-string and
        remain elements are fields of the task: ID, date of the task's creation,
        title, task description"""

        _, date_until = dates_period
    
        query_set = models.Task.objects\
            .select_related('interval')\
            .values_list('interval__interval', 'ID', 'title',\
                         'initdate', 'description')\
            .filter(interval__isnull=False, initdate__lt=date_until)\
            .exclude(interval__interval='no')\

        return list(query_set)

    @staticmethod
    def get_additional_fields(task_IDs_list):
        """ Takes a list of task IDs and extracts data from tables that 
        contains additional information about each task with the given ID.
            Returns a list of tuples containing the task's ID, task's 
        completion date, and files associated with the task."""

        # TODO: fix multiple files for single task situation 
        query_set = models.Task.objects\
            .select_related('completion', 'file')\
            .values_list('ID', 'completion__date_when', 'file__ID',\
                         'file__link', 'file__related_task_id')\
            .filter(ID__in=task_IDs_list)
        
        return str(query_set)
    
    @staticmethod
    def add_overall_task(overall_dict):
        """Takes a dict of all fields of the task (arg "overall_dict") 
        and inserts them into related sql tables."""

        new_task = models.Task.objects.create(
            initdate=overall_dict['initdate'],
            title=overall_dict['title'],
            description=overall_dict['description']
        )
        if 'interval' in overall_dict.keys():
            models.Interval.objects.create(
                interval=overall_dict['interval'],
                related_task=new_task   
            )
        if 'completion' in overall_dict.keys():
            models.Completion.objects.create(
                date_when=overall_dict['completion'],
                related_task=new_task
            )
        if 'autoshift' in overall_dict.keys():
            models.Autoshift.objects.create(
                value=overall_dict['autoshift'],
                related_task=new_task
            )
        # TODO: adding in db attached files

    def update_overall_task(self):
        pass

    def delete_task(self):
        pass

    def check_uncheck_task(self):
        pass

    def shift_tasks(self):
        pass









