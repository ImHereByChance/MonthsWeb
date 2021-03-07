from .dateservice import DatesHandler, RepeatingTasksGenerator
from datetime import date, datetime


class TaskHandler:
    """Retrieve the tasks form database, make copies of tasks if it must
    repeat according to certain time interval and another hard logic
    related to the user tasks entities"""
    
    def __init__(self, db_service):
        # an objects which can handle the database records about Task,
        # Completion and File entities. Should have methods listed in
        # self._is_db_service_valid(self, db_service) to work well.
        self.db_service = db_service
        
        if not self._is_db_service_valid(db_service):
            raise ValueError('invalid value of the db_service argument')
    
    #                            ***
    #                           public

    def generate_tasklist_for_dates(self, monthdates_objects: list) -> list:
        """Takes a list of `datetime.datetime` objects and returns a
        list of ALL tasks (as dicts) that appears on those dates (their
        interval settings).
        """
        # tuple of first and last date in the month
        date_range = (monthdates_objects[0], monthdates_objects[-1])
        
        tasks_by_interval = self._get_tasks_by_intervall(monthdates_objects)
        tasks_by_month = self._get_tasks_by_month(date_range)

        tasks_total = tasks_by_month + tasks_by_interval

        if tasks_total:
            tasks_total = self._add_remain_fields(tasks_total)
            tasks_total =  self._convert_dates_to_strings(tasks_total)

        return tasks_total

    #                           ***
    # ancillary methods for self.generate_tasklist_for_dates() method

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
            # adding fielsd with default values
            task['files'] = []
            task['completion'] = False
            # append files in list of task['files']
            for file_ in additional_fields['files']:
                if file_['related_task_id'] == task['id']:
                    task['files'].append(file_)
            # if date is marked as completed on it's ['date'],
            # set ['completion'] = ['date'] 
            for completion in additional_fields['completions']:
                if (completion['date_completed'].date() == task['date'].date()
                        and completion['related_task_id'] == task['id']):
                    task['completion'] = completion['date_completed']
                    break

        return task_dicts
    
    def _convert_dates_to_strings(self, task_dicts: list) -> list:
        """Takes a list of task (as dicts) and convert all `datetime`
        objects in it ISOformat date-strings (recursively, including
        nested arrays).
        """
        for dct in task_dicts:
            for key, value in dct.items():    
                # recursive convertion of nested containers
                if type(value) in [list, tuple, set]:
                    self._convert_dates_to_strings(value)
                elif (isinstance(value, datetime)):
                    dct[key] = value.isoformat()
        # now task dicts finally compled and can be sent to the client
        return task_dicts

    #                       ***
    #                      other
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
