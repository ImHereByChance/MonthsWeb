from .dateservice import DatesHandler, RepeatingTasksGenerator
from datetime import date, datetime


class TaskHandler:
    def __init__(self, db_service):
        # an objects which can handle the database records about Task,
        # Completion and File entities. Should have methods listed in
        # self._is_db_service_valid(self, db_service) to work well.
        self.db_service = db_service
        
        if not self._is_db_service_valid(db_service):
            raise ValueError('invalid value of the db_service argument')

    def _is_db_service_valid(self, db_service):
        """Check the consistens of the service class object which
        handles database."""

        obligatory_attrs = [
            'get_intervalled_tasks',
            'get_monthly_tasks',
            'get_additional_fields'
        ]
        for attr in obligatory_attrs:
            if not hasattr(db_service, attr):
                return False
        return True 

    def _get_tasks_by_intervall(self, datetime_objects: list) -> list:
        """Takes a list of datetime.datetime objects and returns a list
        of tasks (as dicts) that appears on those dates according to
        their interval settings.
        """
        # extract first and last dates from datetime_objects
        date_range = datetime_objects[0], datetime_objects[-1]
        
        intervalled_tasks = self.db_service.get_intervalled_tasks(date_range)
        matched = RepeatingTasksGenerator.generate(
            datetime_objects=datetime_objects,
            intervalled_tasks=intervalled_tasks
        )
        return matched

    def _get_tasks_by_month(self, date_range: tuple) -> list:
        """Takes a list of datetime objects and returns a list of
        dictionaries with task for those dates (excluding interval
        tasks).
        """
        monthly_tasks = self.db_service.get_monthly_tasks(date_range)
        # need to add actual task's date, which is the same as task's creation
        # date (init_date) if the task is not intervalled (like these).
        for dct in monthly_tasks:
            dct['date'] = dct['init_date']
        return monthly_tasks

    def _add_remain_fields(self, task_dicts: list) -> list:
        """ Takes list of Tasks and add to them fields that requires
        additional request to database: "files", "completion"."""
        task_id_list = set(task_dict['id'] for task_dict in task_dicts)
        additional_fields = self.db_service.get_additional_fields(task_id_list)
        
        for task in task_dicts:
            task['files'] = []
            task['completion'] = False
            for file_ in additional_fields['files']:
                if file_['related_task_id'] == task['id']:
                    task['files'].append(file_)
            for completion in additional_fields['completions']:
                if (completion['date_completed'].date() == task['date'].date()
                        and completion['related_task_id'] == task['id']):
                    task['completion'] = completion['date_completed']
                    break        
        return task_dicts
    
    def _convert_dates_to_strings(self, task_dicts: list) -> list:
        for dct in task_dicts:
            for key, value in dct.items():    
                # recursive convertion of nested containers
                if type(value) in [list, tuple, set]:
                    self._convert_dates_to_strings(value)
                elif (isinstance(value, datetime)):
                    dct[key] = value.isoformat()
        
        return task_dicts
                 

    
    def get_monthly_tasks(self, monthdates_objects):
        # tuple of first and last date in the month
        date_range = (monthdates_objects[0], monthdates_objects[-1])

        tasks_total = from_intervals + from_monthdate

        if tasks_total:
            self.add_remain_fields(tasks_total)

        return tasks_total



    # ???
    def add_task_to_db(self, task_dict):
        self.db_service.add_overall_task(task_dict)

    def upd_task_in_db(self, task_dict):
        self.db_service.update_overall_task(task_dict)

    def del_task_from_db(self, task):
        """can accept as an arg task dictionary or integer task id"""
        self.db_service.delete_task(task)

    def check_uncheck_task(self, task_dict):
        self.db_service.check_uncheck_task(task_dict)

    def shift_tasks(self):
        today_str = DatesHandler.get_today()  # TODO: fix it. DatesHandler is rewritten
        self.db_service.shift_tasks(today_str)


class Package():
    """A dispatcher class responsible for collecting packages from the outputs
    of other service classes (Dates_handler, Interval_handler, Db_handler)
    to wrap them in a single json response and it them to the client.
    """

    def __init__(self, task_service):
        self.task_service = task_service

    def for_new_month(self, date_string):
        monthdates_objects = DatesHandler.generate_month_dates(date_string,
                                                      as_objects=True)
        monthdates = [DatesHandler.to_localestring(obj)  # TODO: fix it. DatesHandler is rewritten
                             for obj in monthdates_objects]

        tasks_objs = self.task_service.get_monthly_tasks(date_string,
                                                         monthdates_objects)
        tasks_dicts = [task.fields_dict for task in tasks_objs]

        package = {'monthdates': monthdates, 'tasks': tasks_dicts}

        return package
