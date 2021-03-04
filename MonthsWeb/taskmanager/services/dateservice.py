import calendar
import datetime
from collections import namedtuple
import pytz
from dateutil.rrule import *
from django.utils import timezone


class DatesHandler:
    """ self explanatory """
    
    @staticmethod
    def is_end_of_month(dt_obj):
        """ Checks whether a datetime.date or datetime.datetime object
        falls on the last day of it's appropriate month.
        """
        if dt_obj.day not in (28, 29, 30, 31):
            return False
        try:
            dt_obj.replace(day=dt_obj.day + 1)
        except ValueError:
            return True
        else:
            return False

    @staticmethod
    def get_monthdates(date:str , as_objects=False):
        """ Takes a date string in ISOformat (e.g. '2022-05-06T00:00:00+00:00')
        or datetime.datetime/datetime.date object and returns a list of
        appropriate month's date-strings in ISOformat or if, flag as_objects is
        True, list of datetime.datetime.objects. Timezones support included.
        """
        if isinstance(date, str):
            try:
                date = timezone.datetime.fromisoformat(date)
            except Exception as e:
                raise e
        elif (isinstance(date, datetime.datetime) or
              isinstance(date, datetime.date)):
            pass
        else:
            raise TypeError('argument should be a date string in ISOformat ',
                            '(e.g. "2022-05-06T00:00:00+00:00") or ',
                            'datetime.datetime/datetime.date object')

        c = calendar.Calendar()
        datetimes_gen = c.itermonthdates(date.year, date.month)
        monthdates = [i for i in datetimes_gen]
        last_date = monthdates[-1]
        # adds more one (two) week from next month in order to
        # prevent empty space on calendar widget bottom
        if len(monthdates) < 42:
            if date.month == 12:
                month = 1
                year = date.year + 1
            else:
                month = date.month + 1
                year = date.year

            next_datetimes_gen = c.itermonthdates(year, month)
            next_monthdates = [i for i in next_datetimes_gen]

            # the last date doesn't come up on the middle of the week,
            # therefore need to add second week from the next week
            if date.month != last_date.month:
                extra_days = next_monthdates[7:14]
            # the last date come up on the last day of the week
            elif date.month == last_date.month:
                # if it's February, that begins on Monday and ends on Sunday
                # it'll contain only 28 dates and demands two additional weeks
                if len(monthdates) == 28:
                    extra_days = next_monthdates[0:14]
                # last date come up on the middle of the week
                # and it already completed by Calendar module.
                # Needs 2d week from the next month.
                else:
                    extra_days = next_monthdates[0:7]
            else:
                raise ValueError('unexpected situation while adding extra days ',
                                 'from next month to pageDaysArr')
            monthdates += extra_days

        # list of datetime.date to django.utils.timezone() with timezone +00:00
        aware_datetimes_list = [
            timezone.make_aware(
                value=datetime.datetime(date.year, date.month, date.day),
                timezone=pytz.timezone('Etc/GMT+0')
            )
            for date in monthdates
        ]
        
        if as_objects:
            return aware_datetimes_list
        else:
            return [dt.isoformat() for dt in aware_datetimes_list]


class IntervalHandler:
    """TODO: docstring for this class"""
    # a task that repeats according to the interval settings. For example,
    # a task with the interval 'every day' can have a creation date(init_date)
    # of 01.01.2021 and an actual date of 01.02.2021 etc. In the database
    # stored only the "core-task" with it's creation date. Repeatable
    # "interval" tasks are generated in this class and look like a tuple below.
    # (actual date added to the end).
    Repeated_task = namedtuple(typename='repeated_task',
                               field_names='id, init_date, title, description,'
                                           'interval, autoshift, date')

    @classmethod
    def get_from_montharray(cls, datetime_objects, intervalled_tasks):
        """ Takes a list of datetime.datetime objects as the first argument
        and a list of namedtuples containing intervalled task's fields retrieved
        from the database (via dbservice.DatabaseHandler.get_intervalled_tasks)
            The method checks in a loop whether the task should appear on a
        specific day from the list of datetime objects (specified as the first
        argument) using method is_match of the current class.
            Returns list of namedtuples consisting with following fields: id,
        init_date (date of task creation), title, description, interval, 
        autoshift, date (task's current date which can defer from the task
        creation date).
        """

        list_of_matched = []
        for date_obj in datetime_objects:
            for task in intervalled_tasks:  # each task is namedtuple 
                if cls.is_match(interval=task.interval,
                                init_date=task.init_date,
                                checkdate=date_obj):  
                                # options=options) - TODO
                    matched = cls.Repeated_task(*task, date_obj)
                    list_of_matched.append(matched)
        return list_of_matched

    @classmethod
    def is_match(cls, interval, init_date, checkdate, options=None):
        """ Checks whether the date is within the time interval or not.
        If the interval is simple (such as every_day, every_week etc.,
        i.e. there is no need to use dateutil library), a function needs as
        arguments only the date of task creation and the date, that needs to 
        be checked - otherwise must be provided "options" arg, that contains 
        parameters for dateutil.rrule.
        """    
        intervals_map = {
            'every_day': cls.every_day,
            'every_workday': cls.every_workday,
            'every_week': cls.every_week,            
            'every_month': cls.every_month,
            'every_year': cls.every_year,
            'special': cls.special
        }
        check_func = intervals_map[interval]
        
        if not interval.startswith('special'):
            return check_func(init_date, checkdate)
        elif not options:
            raise TypeError('special time interval needs the options dict '
                            'as arguments of function')
        else:
            return check_func(init_date, checkdate, options)

    #                        ***
    # Flags that returns True if a date match the interval,
    # otherwise returns False. Date when the Task was created
    # (init_date) not included and will return as False.

    @classmethod
    def every_day(cls, init_date, checkdate):
        if init_date.date() >= checkdate.date():
            return False
        else:
            return True

    @classmethod
    def every_workday(cls, init_date, checkdate):
        """ every MONDAY - FRIDAY """
        if init_date.date() >= checkdate.date():
            return False
        elif checkdate.weekday() in (0, 1, 2, 3, 4):
            return True
        else:
            return False

    @classmethod
    def every_week(cls, init_date, checkdate):
        if init_date.date() >= checkdate.date():
            return False
        elif init_date.weekday() == checkdate.weekday():
            return True
        else:
            return False

    @classmethod
    def every_month(cls, init_date, checkdate):
        """(!) if the month of the initial task date is the 31s
        and a checking month have only 30 days - interval will match the 30th
        """
        is_end_of_month = DatesHandler.is_end_of_month

        if init_date.date() >= checkdate.date():
            return False
        elif init_date.day == checkdate.day:
            return True
        elif checkdate.day in (28, 29, 30) and is_end_of_month(checkdate):
            if init_date.day > checkdate.day:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def every_year(cls, init_date, checkdate):
        if init_date.date() >= checkdate.date():
            return
        if (init_date.month, init_date.day) == (checkdate.month, checkdate.day):
            return True
        elif (init_date.month, checkdate.month) == (2, 2):
            if checkdate.day == 28 and DatesHandler.is_end_of_month(checkdate):
                if init_date.day > checkdate.day:
                    return True
            return False
        else:
            return False

    @classmethod
    def special(cls, init_date, checkdate, options):
        pass  # TODO