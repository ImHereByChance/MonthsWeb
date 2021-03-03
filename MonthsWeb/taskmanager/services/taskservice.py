from .dateservice import DatesHandler, IntervalHandler
from django.utils import timezone


class TaskHandler:
    def __init__(self, db_service):
        self.db_service = db_service
        
    def _get_intervalled_tasks_dicts(self, datetime_objects, 
                                     dates_period: tuple) -> dict:
        intervalled_tasks = self.db_service.get_intervalled_tasks(dates_period)
        matched = IntervalHandler.get_from_montharray(
            datetime_objects=datetime_objects,
            intervalled_tasks=intervalled_tasks)
        # convert namedtuples to dicts
        dicts_list = [named_tup._asdict() for named_tup in matched]
        # convert datestrings to datetime objects
        for dct in dicts_list:
            dct['init_date'] = dct['init_date'].isoformat()
            dct['date'] = dct['date'].isoformat()
        
        return dicts_list
            

            




    def get_monthly_tasks(self, monthdates_objs):
        # tuple of first and last date in the month
        dates_period = (monthdates_objs[0], monthdates_objs[-1])

        
        
        # in separate method
        monthly_tasks = self.db_service.get_monthly_tasks(dates_period)

        from_monthdate = []
        for task_tup in monthly_tasks:
            date = task_tup[1]
            interval = task_tup[-1]
            positional_fields = task_tup[:-1]
            task = TaskOverall(date, *positional_fields, interval=interval)
            from_monthdate.append(task)


        tasks_total = from_intervals + from_monthdate

        if tasks_total:
            self.add_remain_fields(tasks_total)

        return tasks_total





    def add_remain_fields(self, task_list):
        """ takes list of Tasks and add to them fields that requires
        additional request to database: "files", "completion". """
        task_IDs_list = set(task.ID for task in task_list)
        additional_fields = self.db_service.get_additional_fields(task_IDs_list)

        for task in task_list:
            for field in additional_fields:
                field_id = field[0]
                completion = field[1]
                file_id, file_link, file_task_id = field[2:]

                if task.ID == field_id:
                    if file_task_id == task.ID:
                        file = File(file_id, file_link, file_task_id)
                        task.attach_file(file.fields_dict)

                    if completion == task.date:
                        task.completion = completion



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
    to wrap them in a single json response and it them to the client."""

    def __init__(self, task_service):
        self.task_service = task_service

    def for_new_month(self, date_string):
        monthdates_objs = DatesHandler.get_monthdates(date_string,
                                                      as_objects=True)
        monthdates = [DatesHandler.to_localestring(obj)  # TODO: fix it. DatesHandler is rewritten
                             for obj in monthdates_objs]

        tasks_objs = self.task_service.get_monthly_tasks(date_string,
                                                         monthdates_objs)
        tasks_dicts = [task.fields_dict for task in tasks_objs]

        package = {'monthdates': monthdates, 'tasks': tasks_dicts}

        return package
