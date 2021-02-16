from .dateservice import DatesHandler, IntervalHandler

class TaskOverall:
    """docstring for Task"""

    def __init__(self, date, ID, initdate, title, description,
                 autoshift='no', completion=False, interval='no', files=None):
        self.date = date
        self.ID = ID
        self.initdate = initdate
        self.title = title
        self.description = description
        self._interval = interval
        self._autoshift = autoshift
        self.completion = completion
        if files is None:
            self.files = []
        else:
            self.files = files

    def __repr__(self):
        if self.date == self.initdate:
            interval_info = 'not from interval'
        else:
            interval_info = 'from interval'
        return f'<Task__id:_{self.ID}__{interval_info}>'

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, setting_value):
        if self._autoshift and setting_value:
            raise ValueError('task may have either interval or autoshift ',
                             'properties - not both of them')
        self._interval = setting_value

    @property
    def autoshift(self):
        return self._autoshift

    @autoshift.setter
    def autoshift(self, setting_value):
        if self._interval and setting_value:
            raise ValueError('task may have either interval or autoshift ',
                             'properties - not both of them')
        self._autoshift = setting_value

    @property
    def fields_dict(self):
        proper_dict = {}
        for k in self.__dict__:
            if k.startswith('_'):
                key = k[1:]
                value = self.__dict__[k]
                proper_dict[key] = value
            else:
                proper_dict[k] = self.__dict__[k]
        return proper_dict

    def attach_file(self, *files):
        """Adds to self.files list dicts, that represents fields
        of 'file' database entries."""
        for new_file in files:
            if tuple(new_file.keys()) == ('ID', 'link', 'task_id'):
                pass
            else:
                raise TypeError('File object should be a dict with ',
                                'appropriate keys: "ID", "link", "task_id"')

            if new_file in self.files:
                continue

            self.files.append(new_file)


class File:
    """An object for working with data about files attached to specific tasks."""
    def __init__(self, ID, link, task_id):
        self.ID = ID
        self.link = link
        self.task_id = task_id

    def __repr__(self):
        return f'File_link_with_path:_{self.link} '

    @property
    def fields_dict(self):
        return self.__dict__


class TaskHandler:
    def __init__(self, db_service):
        self.db_service = db_service

    def get_monthly_tasks(self, date_string, monthdates_objs):
        # tuple of first and last date in the month
        dates_period = DatesHandler.get_dates_period(monthdates_objs)

        intervalled_tasks = self.db_service.get_intervalled_tasks(dates_period)
        matched = IntervalHandler.get_from_montharray(
            monthdates_objs=monthdates_objs,
            intervalled_tasks=intervalled_tasks)

        from_intervals = []
        for tup in matched:
            date, interval, task_fields = tup
            date = DatesHandler.to_localestring(date)
            task = TaskOverall(date, *task_fields, interval=interval)
            from_intervals.append(task)

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
        today_str = DatesHandler.get_today()
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
        monthdates = [DatesHandler.to_localestring(obj)
                      for obj in monthdates_objs]

        tasks_objs = self.task_service.get_monthly_tasks(date_string,
                                                         monthdates_objs)
        tasks_dicts = [task.fields_dict for task in tasks_objs]

        package = {'monthdates': monthdates, 'tasks': tasks_dicts}

        print(f'Made new month pack for date {date_string}:')
        count = 1
        for task in tasks_dicts:
            number_files = len(task['files'])
            print(f'{count}){task}, attached files: {number_files}')
            count += 1
        print('***')

        return package