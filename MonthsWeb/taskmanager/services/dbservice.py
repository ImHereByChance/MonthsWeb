from django.db.models import CharField
from django.db.models.functions import Cast
from django.utils import timezone
from ..models import Task, File, Completion
from collections import namedtuple


class DatabaseHandler:
    # fields, stored in the taskmanager.models.Task 
    Core_fields = namedtuple(typename='Core_fields',
                             field_names=('id, init_date, title, description,'
                                          'interval, autoshift'))
    # fields, stored in the related to taskmanager.models.Task via Foreign key
    # models: taskmanager.models.Completion and taskmanager.models.File
    Additional_fields = namedtuple(typename='Additional_fields',
                                   field_names=('id, completion,' 
                                                'file__id, file__link,' 
                                                'file__related_task_id'))

    @classmethod
    def get_monthly_tasks(cls, dates_period: tuple):
        """Takes a tuple of two datetime objects and retrieves from database
        all the tasks (all fields including fields from related tables), that
        matches this time period (except the fields, which can be multiple for 
        each task.ID: "completion" and "file")
        """
        values_list = Task.objects\
            .values_list('id',
                         'init_date',
                         'title',
                         'description',
                         'interval',
                         'autoshift')\
            .filter(init_date__range=dates_period)

        return [cls.Core_fields(*tup) for tup in list(values_list)]

    @classmethod
    def get_intervalled_tasks(cls, dates_period: tuple):
        """ Takes a tuple of two datetime objects, where the first is the
        beginning- and the second is the end- of the time period. The method
        finds all interval-based tasks that matches the period and returns a
        list of tuples with following items: id, date of the task's creation,
        title, task, description, interval (e.g. "every_day", "every_month" 
        etc),  information about autoshift.
        """
        _, date_until = dates_period  # needs only end-date of period

        values_list = Task.objects\
            .values_list('id',
                         'init_date',
                         'title',
                         'description',
                         'interval',
                         'autoshift')\
            .filter(init_date__lt=date_until)\
            .exclude(interval='no')

        return [cls.Core_fields(*tup) for tup in list(values_list)]

    @classmethod
    def get_additional_fields(cls, task_IDs_list: list):
        """ Takes a list of task IDs and extracts data from tables that
        contains additional information about each task with the given ID.
        Returns a list of tuples containing the task's ID, task's completion
        date, and files associated with the task.
        """
        values_list = Task.objects\
            .select_related('completion', 'file')\
            .values_list(
                'id',                              # as a string ↴
                Cast('completion__date_completed', output_field=CharField()),
                'file__id',
                'file__link',
                'file__related_task_id')\
            .filter(id__in=task_IDs_list)

        return [cls.Additional_fields(*tup) for tup in list(values_list)]

    @staticmethod
    def add_overall_task(overall_dict: dict):
        """Takes a dict of all fields of the task (arg "overall_dict") 
        and inserts them into database.
        """
        # isostring to datetime object
        task_creation_time = timezone.datetime.fromisoformat(
            overall_dict['init_date'])
        # TODO: fix
        if overall_dict['autoshift'] == 'no':
            overall_dict['autoshift'] = False
        elif overall_dict['autoshift'] == 'yes':
            overall_dict['autoshift'] = True

        Task.objects.create(init_date=task_creation_time,
                            title=overall_dict['title'],
                            description=overall_dict['description'],
                            interval=overall_dict['interval'],
                            autoshift=overall_dict['autoshift'])

        # TODO: adding in db attached files

    @staticmethod
    def update_overall_task(overall_dict: dict):
        """ Takes a dict of all fields of the task and updates it by id."""
        # copy to not to mutate original dict
        updated_dict = {k: v for k, v in overall_dict.items()}

        # filter non required fields that may cause KeyError
        non_required = []
        for key in updated_dict.keys():
            if key not in ['id', 'init_date', 'title',
                           'description', 'interval', 'autoshift']:
                non_required.append(key)
        if non_required:
            for k in non_required:
                del updated_dict[k]

        # ISOstring to datetime
        if updated_dict['init_date']:
            updated_dict['init_date'] = timezone.datetime\
                .fromisoformat(overall_dict['init_date'])

        # Update fields
        Task.objects\
            .filter(id=overall_dict['id'])\
            .update(**updated_dict)

        # TODO: attached files

    @staticmethod
    def delete_task(task):
        """ Delete task by id from database (including all related to it via
        foreign key). As an argument can be provided a dict, that contains
        {'id': <integer id>} key-value pair or direct integer id value
        """
        if isinstance(task, dict):
            task_id = task['id']
        elif isinstance(task, int):
            task_id = task
        else:
            raise TypeError('the argument must be type of dict or int')

        Task.objects.filter(id=task_id).delete()

    @staticmethod
    def check_uncheck_task(task_dict: dict):
        """ Creates an entry in the "Completion" table if
        task_dict['completion'] have a value (it must be a datetime str
        formated as "2020-01-01 00:00:00"). If task_dict['completion'] == False
        - deletes appropriate entry about task complition.
        """
        task_id = task_dict['id']
        completion = task_dict['completion']
        task_date = timezone.datetime.fromisoformat(task_dict['date'])
        if completion:
            completion = timezone.datetime.fromisoformat(completion) 
            Completion.objects.create(
                date_completed=completion,
                related_task_id=task_id)
        else:
            try:
                Completion.objects.filter(
                    date_completed__date=task_date.date(),
                    related_task_id=task_id).delete()
            except Completion.DoesNotExist:
                pass

    @staticmethod
    def shift_tasks(today):
        """Changes the date of the uncompleted Tasks with Autoshift=True 
        to the given date (shifts them to today if them not completed yet)"""
        nested_query = Completion.objects.values_list('id', flat=True)\
            .filter(date_completed__date__lt=today.date())
        query = Task.objects\
            .prefetch_related('completion')\
            .filter(init_date__date__lt=today.date())\
            .exclude(autoshift=False)\
            .exclude(id__in=nested_query)\
            .update(init_date=today)
