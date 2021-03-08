import calendar
import datetime
import pytz
from django.utils import timezone
from typing import Union


class DatesHandler:
    """ Class for hard logic related to dates and time."""
   
    @staticmethod
    def is_end_of_month(dt_obj: datetime) -> False:
        """ Is this `datetime` object the last day of it's month?"""
        if dt_obj.day not in (28, 29, 30, 31):
            return False
        try:
            dt_obj.replace(day=dt_obj.day + 1)
        except ValueError:
            return True
        else:
            return False

    @staticmethod
    def generate_month_dates(date: Union[str, datetime.datetime], 
                             as_objects: bool = False) -> list:
        """ 1. Takes a date-string in ISOformat (e.g. 
        '2022-05-06T00:00:00+00:00') or `datetime` object.
        2. Extracts the month from the given date.
        3. Return a list of all days in this month as ISOstrings
        (by default) or `as_objects` datetime. 
            
        List contains extra-days to make 6 full weeks and look as
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
        # initialize calendar and make list of dates of the given month
        # and extra-days to make 6 full weeks of this month.
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