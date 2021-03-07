import calendar
import datetime
import pytz
from dateutil.rrule import *
from django.utils import timezone
from typing import Union


class DatesHandler:
    """ Class for hard logic related to dates and time."""
   
    @staticmethod
    def is_end_of_month(dt_obj: datetime) -> False:
        """ Are you the last day of your month, "datetime.datememe"?"""
        if dt_obj.day not in (28, 29, 30, 31):
            return False
        try:
            dt_obj.replace(day=dt_obj.day + 1)
        except ValueError:
            return True
        else:
            return False

    @staticmethod
    def  generate(date: Union[str, datetime.datetime], 
                         as_objects: bool = False) -> list:
        """ 1. Take a date string in ISOformat (e.g. 
        '2022-05-06T00:00:00+00:00') or `datetime` object.
        2. Extract the month from the given date.
        3. Return a list of all days in this month as ISOstrings
        (by default) or `as_objects` datetime. 
            
        List contains extra-days dates to make 6 full weeks and look as
        pretty a calendar: 

             January(2020)                   
        Mo Tu We Th Fr Sa Su  \n
        30 31  1  2  3  4  5  \n
         6  7  8  9 10 11 12  \n
        13 14 15 16 17 18 19  \n
        20 21 22 23 24 25 26  \n
        27 28 29 30 31  1  2  \n
         3  4  5  6  7  8  9  \n
        ```
        # Example of usage:
        >>> generate(date=datetime.date(2020, 1, 1))
        
        ["2019-12-30T00:00:00+00:00",
         "2019-12-31T00:00:00+00:00",
         "2020-01-01T00:00:00+00:00",
         ...                          
         "2020-03-09T00:00:00+00:00" ]
        """
        # input types checking
        try:
            if isinstance(date, str):
                date = timezone.datetime.fromisoformat(date)
            elif (isinstance(date, datetime.datetime) or
                  isinstance(date, datetime.date)):
                pass
        except TypeError as err:
            raise err('argument should be a date string in ISOformat ',
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


class RepeatingTaskGenerator:
    """ If task repeat according to user-defined time interval,
    this class generates the copies of such task for each date when
    it should be repeated.
    """
    
    @classmethod
    def generate(cls, datetime_objects: list,
                 intervalled_tasks: list) -> list:
        """ 1 Takes:
        1) list of `datetime_objects`
        2) list of user-made tasks (as dicts) which must be repeated
        according to specified `task['interval']` (e.g 'every_day',
        'every_workday' etc.).
    
        2 Returns list of tasks (as dicts) with new key ['date'], that
        denote when task should be repeated (task creation date -
        `['init_date']` is not included)
        """
        list_of_matched = []
        for date_obj in datetime_objects:
            for task in intervalled_tasks:
                if cls._is_match(task=task, checkdate=date_obj):
                    matched_dict_copy = {k:v for k,v in task.items()}
                    matched_dict_copy['date'] = date_obj
                    list_of_matched.append(matched_dict_copy)

        return list_of_matched

    @classmethod
    def _is_match(cls, task: dict, checkdate: datetime.datetime) -> bool:
        """ Checks whether the task with interval settings should
        appear on particular date(checkdate arg) or not.
        """    
        intervals_map = {
            'every_day': cls._every_day,
            'every_workday': cls._every_workday,
            'every_week': cls._every_week,            
            'every_month': cls._every_month,
            'every_year': cls._every_year,
            'special': cls._special
        }
        interval = task['interval']
        init_date = task['init_date']
        options = None  # TODO: fix when complex intervals will be implemented
        check_func = intervals_map[interval]
        
        if not interval.startswith('special'):
            return check_func(init_date, checkdate)
        elif not options:
            raise TypeError('special time interval needs the options dict '
                            'as arguments of function')
        else:
            return check_func(init_date, checkdate, options)

    @classmethod
    def _every_day(cls, init_date: datetime.datetime,
                   checkdate:datetime.datetime) -> None:
        """ Returns `True` if `checkdate` matches 'every_day', interval.
        Otherwise returns False. Date when the Task was created
        (`init_date`) always returns as `False`.
        """
        if init_date.date() >= checkdate.date():
            return False
        else:
            return True

    @classmethod
    def _every_workday(cls, init_date: datetime.datetime,
                       checkdate:datetime.datetime) -> None:
        """ Returns `True` if `checkdate` matches 'every_workday'
        interval (every MONDAY-FRIDAY). Otherwise returns `False`.
        Date when the Task was created (`init_date`) always returns
        as `False`.
        """
        if init_date.date() >= checkdate.date():
            return False
        elif checkdate.weekday() in (0, 1, 2, 3, 4):
            return True
        else:
            return False

    @classmethod
    def _every_week(cls, init_date: datetime.datetime,
                    checkdate:datetime.datetime) -> None:
        """ Returns `True` if `checkdate` match interval 'every_week',
        otherwise returns False. Date when the Task was created
        (`init_date`) always returns as `False`.
        """
        if init_date.date() >= checkdate.date():
            return False
        elif init_date.weekday() == checkdate.weekday():
            return True
        else:
            return False

    @classmethod
    def _every_month(cls, init_date: datetime.datetime,
                     checkdate:datetime.datetime) -> None:
        """ Returns `True` if `checkdate` match interval 'every_month',
        otherwise returns False. Date when the Task was created
        (`init_date`) always returns as `False`.
        
        If the month of the `init_date` is 31 and a checking month have
        only 30 or less days returns `True` on the latest date of the
        month.
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
    def _every_year(cls, init_date: datetime.datetime,
                    checkdate:datetime.datetime) -> None:
        """ Returns `True` if `checkdate` matches 'every_year',
        interval. Otherwise returns `False`. Date when the Task was created
        (`init_date`) always returns as `False`.
        """
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
    def _special(cls, init_date, checkdate, options):
        pass  # TODO
