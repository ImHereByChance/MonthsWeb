from ..models import Task, File, Completion
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class DatabaseHandler:
    """ Select, create, update, delete and other interactions
    with database.
    """
    
    @staticmethod
    def get_tasks_by_timerange(date_range: tuple, user: User) -> list:
        """Retrieve from database all `models.Task` in given time range
        (related models `Completion` and `File` are not touched). 
        """
        retrieved_values = Task.objects\
            .values('id',
                    'init_date',
                    'title',
                    'description',
                    'interval',
                    'autoshift')\
            .filter(init_date__range=date_range, user=user)

        return list(retrieved_values)

    @staticmethod
    def get_intervalled_tasks(date_range: tuple, user: User) -> list:
        """ 1. Takes a tuple of two `datetime` objects, where the first
        is the beginning- and the second is the end- of the time period
        2. Returns list of all interval-based tasks in the given
        `date_range`.
        """
        _, date_until = date_range  # needs only end-date of period

        retrieved_values = Task.objects\
            .values('id',
                    'init_date',
                    'title',
                    'description',
                    'interval',
                    'autoshift')\
            .filter(init_date__lt=date_until, user=user)\
            .exclude(interval='no')

        return list(retrieved_values)

    @staticmethod
    def get_additional_fields(task_id_list: list) -> dict:
        """ Takes a list of models.Task id-s - returns the dict of
        two keys:

        1) ['files'] (list of attached files);
        2) ['completions'] (`datetime.datetime`s when the task was
           marked as completed). 
        """
        files = File.objects\
            .values('id', 'link', 'related_task_id')\
            .filter(related_task_id__in=task_id_list)
        completions = Completion.objects\
            .values('id', 'date_completed', 'related_task_id')\
            .filter(related_task_id__in=task_id_list)
            
        additional_fields = {
            'files': list(files),
            'completions': list(completions)
        }
        return additional_fields

    @staticmethod
    def create_task_and_related(task_and_related: dict, user: User) -> None:
        """Takes a dict where the keys are the fields of
        `models.Task` and related models `File`, `Completion`,
        and inserts the into database.
        """
        # ISOstring to datetime object
        task_creation_date = timezone.datetime.fromisoformat(
                task_and_related['init_date'])
        # insert Task
        created_task = Task.objects.create(
                init_date=task_creation_date,
                title=task_and_related['title'],
                description=task_and_related['description'],
                interval=task_and_related['interval'],
                autoshift=task_and_related['autoshift'],
                user=user
        )
        # create attached File models
        try:
            for file_ in task_and_related['files']:
                File.objects.create(related_task=created_task,
                                    link=file_['link'])
        except KeyError:
            pass

    @staticmethod
    def update_task_and_related(task_and_related: dict) -> None:
        """ Takes a dict of all fields of the Task and updates this
        model by id (with related models File and Comletion).
        """
        # copy to not to mutate original dict
        updated_dict = {k: v for k, v in task_and_related.items()}

        # filter non required fields that may cause KeyError
        non_required = []
        for key in updated_dict.keys():
            if key not in ['id', 'init_date', 'title', 'description',
                           'interval', 'autoshift']:
                non_required.append(key)
        if non_required:
            for k in non_required:
                del updated_dict[k]

        # ISOstring to datetime
        if updated_dict['init_date']:
            updated_dict['init_date'] = timezone.datetime\
                .fromisoformat(task_and_related['init_date'])

        # Update fields
        Task.objects\
            .filter(id=task_and_related['id'])\
            .update(**updated_dict)

        # TODO: attached files

    @staticmethod
    def delete_task(task: dict) -> None:
        """ Delete a task by id from database (including all related
        to it via foreign key).
        As an argument can be provided a dict, that contains
        {'id': <integer id>} key-value pair or plain integer id of
        the task.
        """
        if isinstance(task, dict):
            task_id = task['id']
        elif isinstance(task, int):
            task_id = task
        else:
            raise TypeError('the argument must be type of dict or int')

        Task.objects.filter(id=task_id).delete()

    @staticmethod
    def check_uncheck_task(task_dict: dict) -> None:
        """ Creates an entry in the "Completion" table if
        task_dict['completion'] have a value (it must be a datetime str
        formated as "2020-01-01 00:00:00"). If
        task_dict['completion'] == False, deletes appropriate entry
        about task complition.
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
                    date_completed__date=task_date,
                    related_task_id=task_id).delete()
            except Completion.DoesNotExist:
                pass

    @staticmethod
    def shift_tasks(today: datetime) -> None:
        """Changes the date of the uncompleted tasks with
        `Autoshift=True` to the given date (shifts them to
        today if they does't completed yet)
        """
        nested_query = Completion.objects.values_list('id', flat=True)\
            .filter(date_completed__date__lt=today.date())
        Task.objects\
            .prefetch_related('completion')\
            .filter(init_date__date__lt=today.date())\
            .exclude(autoshift=False)\
            .exclude(id__in=nested_query)\
            .update(init_date=today)
