from typing import overload
from django.test import TestCase
from django.db.models.fields import AutoField, CharField
from django.db.models.functions import Cast
from django.utils import timezone
from django.db import IntegrityError
from .models import (Task, Completion, File)
from .services.dbservice import DatabaseHandler
from .services.dateservice import DatesHandler


class TestModels(TestCase):
    def setUp(self):
        # do not delete, only add
        task_1 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2021-02-21T16:26:03.850+00:00"),
            title='test task 1',
            description='bare task without interval and autoshift'
        )
        task_2 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2021-02-20T14:01:40.981+00:00"),
            title='test task 2',
            description='task with interval value "every_day"',
            interval='every_week'
        )
        task_3 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2021-02-23T17:59:22.900+00:00"),
            title='test task 3',
            description='task with autoshift value True',
            autoshift=True
        )
        completion_1 = Completion.objects.create(
            date_completed=timezone.datetime.fromisoformat(
                "2021-02-20T16:41:30.981+00:00"),
            related_task=task_2
        )

    def test_task_creation_constraint(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(init_date=timezone.now(),
                                title='nevermind',
                                interval='every_day',  # should be only one
                                autoshift=True)        # of them

    def test_completion_constraint(self):
        existing_model = Completion.objects\
            .select_related('related_task')\
            .get(related_task__title='test task 2')
        with self.assertRaises(IntegrityError):
            # only one for the same date
            Completion.objects.create(
                date_completed=existing_model.date_completed,
                related_task=existing_model.related_task
            )
        with self.assertRaises(IntegrityError):
            slightly_different_time = timezone.datetime.fromisoformat(
                "2021-02-20T17:30:30.000+00:00"
            )
            Completion.objects.create(
                date_completed=slightly_different_time,
                related_task=existing_model.related_task
            )
        with self.assertRaises(IntegrityError):
            slightly_different_time = timezone.datetime.fromisoformat(
                "2021-02-20T15:30:30.000+00:00"
            )
            Completion.objects.create(
                date_completed=slightly_different_time,
                related_task=existing_model.related_task
            )

    # deletes some initialized in seUp() objects. Run it only after all
    # other testcases!
    def test_task_on_delete(self):
        Task.objects.filter(title='test task 3').delete()
        # attached to the 'test task 3' files, that must be delete with it
        files_qset = File.objects.filter(link__in=['file1/for/task/3',
                                                   'file2/for/task/3'])
        self.assertEqual(files_qset.count(), File.objects.none().count())

        Task.objects.filter(title='test task 2').delete()
        completion_qset = Completion.objects.filter(date_completed__in=[
            timezone.datetime.fromisoformat(
                "2021-02-20T16:41:30.981+00:00"),
            timezone.datetime.fromisoformat(
                "2021-03-06T10:10:59.981+00:00")
        ])
        self.assertEquals(first=completion_qset.count(),
                          second=Completion.objects.none().count())


class TestDatabaseHandler(TestCase):
    def setUp(self):
        task_1 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2021-02-21T16:26:03.850+00:00"),
            title='test task 1',
            description='bare task without interval and autoshift'
        )
        task_2 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2021-02-20T14:01:40.981+00:00"),
            title='test task 2',
            description='task with interval value "every_week"',
            interval='every_week'
        )
        task_3 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2021-02-23T17:59:22.900+00:00"),
            title='test task 3',
            description='task with autoshift value True',
            autoshift=True
        )
        task_4 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2021-03-01T17:59:22.900+00:00"),
            title='test task 4',
            description='task which is in next month',
        )
        task_5 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2021-01-01T17:59:22.900+00:00"),
            title='test task 5',
            description='with interval from previous month',
            interval='every_month'
        )
        task_6 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2026-01-01T17:59:22.900+00:00"),
            title='test task 6',
            description='far away.. just to delete',
        )
        task_7 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2028-01-01T17:59:22.900+00:00"),
            title='test task 7',
            description='far away.. just to delete',
        )
        task_8 = Task.objects.create(
            init_date=timezone.datetime.fromisoformat(
                "2021-04-01T17:59:22.900+00:00"),
            title='test task 8',
            description='autoshift in the following month',
            autoshift=True
        )
        file_1 = File.objects.create(
            link='file1/for/task/3',
            related_task=task_3
        )
        file_2 = File.objects.create(
            link='file2/for/task/3',
            related_task=task_3
        )

        completion_1 = Completion.objects.create(
            date_completed=timezone.datetime.fromisoformat(
                "2021-02-21T16:41:30.981+00:00"),
            related_task=task_2
        )
        completion_2 = Completion.objects.create(
            date_completed=timezone.datetime.fromisoformat(
                "2021-03-06T10:10:59.981+00:00"),
            related_task=task_2
        )
        completion_3 = Completion.objects.create(
            date_completed=timezone.datetime.fromisoformat(
                "2021-02-20T18:13:45.436+00:00"),
            related_task=task_1
        )

    def test_get_monthly_tasks(self):
        dates_period = (
            timezone.datetime.fromisoformat(
                "2021-02-01T00:00:00.000+00:00"),
            timezone.datetime.fromisoformat(
                "2021-03-14T21:59:59.999+00:00")
        )

        tuples_list = DatabaseHandler.get_monthly_tasks(dates_period)

        expected_output = [
            (10, '2021-02-21 16:26:03.85+00', 'test task 1',
             'bare task without interval and autoshift', 'no', False),

            (11, '2021-02-20 14:01:40.981+00', 'test task 2',
             'task with interval value "every_week"', 'every_week', False),

            (12, '2021-02-23 17:59:22.9+00', 'test task 3',
             'task with autoshift value True', 'no', True),

            (13, '2021-03-01 17:59:22.9+00', 'test task 4',
             'task which is in next month', 'no', False)
        ]
        # exclude 'id'(index 1) because it can vary depending on case
        self.assertEquals(first=list(i[1:] for i in tuples_list),
                          second=[i[1:] for i in expected_output])

    def test_get_intervalled_tasks(self):
        dates_period = (
            timezone.datetime.fromisoformat(
                "2021-02-01T00:00:00.000+00:00"),
            timezone.datetime.fromisoformat(
                "2021-03-14T21:59:59.999+00:00")
        )

        tuples_list = DatabaseHandler.get_intervalled_tasks(dates_period)

        expected_output = [
            ('every_week', 133, '2021-02-20 14:01:40.981+00', 'test task 2',
             'task with interval value "every_week"', False),

            ('every_month', 136, '2021-01-01 17:59:22.9+00', 'test task 5',
             'with interval from previous month', False)
        ]

        # exclude 'id'(index 1) because it can vary depending on case
        tuples_list = [t[:1] + t[2:] for t in tuples_list]
        expected_output = [t[:1] + t[2:] for t in expected_output]

        self.assertEquals(tuples_list, expected_output)

    def test_additional_field(self):
        dates_period = (
            timezone.datetime.fromisoformat(
                "2021-02-01T00:00:00.000+00:00"),
            timezone.datetime.fromisoformat(
                "2021-03-14T21:59:59.999+00:00"),
        )

        qs = Task.objects.values_list('id').filter(
            init_date__range=dates_period)
        id_set = set(i[0] for i in qs)

        tuples_list = DatabaseHandler.get_additional_fields(id_set)

        expected_output = [
            (10, None, None, None, None),
            (8, '2021-03-06 10:10:59.981+00', None, None, None),
            (9, None, 4, 'file2/for/task/3', 9),
            (9, None, 3, 'file1/for/task/3', 9),
            (7, '2021-02-20 18:13:45.436+00', None, None, None),
            (8, '2021-02-21 16:41:30.981+00', None, None, None)
        ]

        # get rid of any is-s
        tuples_list = [tuple(tup[i] for i in (1, 3)) for tup in tuples_list]
        expected_output = [tuple(tup[i] for i in (1, 3))
                           for tup in expected_output]
        # now check
        self.assertEquals(set(tuples_list), set(expected_output))

    def test_add_overall_task(self):
        # without files
        task1_dict = {
            'id': None,
            'date': "2021-02-01T00:00:00.000+00:00",
            'init_date': "2021-02-01T00:00:00.000+00:00",
            'title': 'created task#1',
            'description': 'no files',
            'interval': 'no',
            'autoshift': False,
        }
        DatabaseHandler.add_overall_task(task1_dict)

        task1_dict_from_db = Task.objects\
            .select_related('completion')\
            .annotate(
                date=Cast('init_date', output_field=CharField()),
            )\
            .values(
                'id',
                'date',
                'title',
                'description',
                'interval',
                'autoshift',
            )\
            .filter(title='created task#1')[0]

        # test equals of dates separately
        self.assertEquals(
            timezone.datetime.fromisoformat(task1_dict['init_date']),
            timezone.datetime.fromisoformat(task1_dict_from_db['date'] + ':00')
        )
        # other fields excluding dates and id
        del task1_dict['id']
        del task1_dict['init_date']
        del task1_dict['date']
        del task1_dict_from_db['id']
        del task1_dict_from_db['date']
        self.assertEquals(task1_dict, task1_dict_from_db)

    def test_update_overall_task(self):
        # without attached files
        task = Task.objects.get(title='test task 1')
        expected_output = {
            'id': task.id,
            'date': '2021-02-16T00:00:00.000+00:00',
            'init_date': '2021-02-16T00:00:00.000+00:00',
            'title': 'updateted task#1',
            'description': '+interval',
            'interval': 'every_month',
            'autoshift': False
        }
        DatabaseHandler.update_overall_task(expected_output)
        updated_dict = Task.objects.values().filter(id=task.id)[0]

        del expected_output['date']
        expected_output['init_date'] = timezone.datetime.fromisoformat(
            expected_output['init_date']
        )

        self.assertEquals(expected_output, updated_dict)

    def test_delete_task(self):
        # delete by overall dict
        task_dict = Task.objects.values().filter(title='test task 6')[0]
        DatabaseHandler.delete_task(task_dict)
        # check
        query_deleted_task = Task.objects.filter(title='test task 6')
        self.assertEquals(list(query_deleted_task), list(Task.objects.none()))

        # by explicit integer id
        task_id = Task.objects.get(title='test task 7').id
        DatabaseHandler.delete_task(task_id)
        # check
        query_deleted_task = Task.objects.filter(title='test task 7')
        self.assertEquals(list(query_deleted_task), list(Task.objects.none()))

    def test_check_uncheck_task(self):
        # CASE#1
        task_id = Task.objects.get(title='test task 4').id
        completion = timezone.datetime.fromisoformat(
            '2021-03-01T19:53:22.900+00:00')
        date = timezone.datetime.fromisoformat('2021-03-01T17:59:22.900+00:00')
        task_dict = {
            'id': task_id,
            'completion': '2021-03-01T19:53:22.900+00:00',
            'date': '2021-03-01T17:59:22.900+00:00'
        }

        DatabaseHandler.check_uncheck_task(task_dict)
        created = Completion.objects.get(related_task_id=task_id,
                                         date_completed=completion)

        self.assertEquals(created.related_task_id, task_id)

        # CASE#2: must delete the previous
        task_dict['completion'] = False
        DatabaseHandler.check_uncheck_task(task_dict)
        test_query = Completion.objects.filter(related_task_id=task_id,
                                               date_completed=completion)
        self.assertFalse(test_query)

        # CASE#3: intervalled task
        task = Task.objects.get(title='test task 2')
        completion = timezone.datetime.fromisoformat(
            "2021-02-27T14:01:40.981+00:00")
        task_dict = {
            'id': task.id,
            'completion': "2021-02-27T14:01:40.981+00:00",
            'date': '2021-02-20T00:00:00.000+00:00'
        }

        DatabaseHandler.check_uncheck_task(task_dict)
        created = Completion.objects.get(related_task_id=task.id,
                                         date_completed=completion)

        self.assertEquals(created.related_task_id, task.id)

    def test_shift_tasks(self):
        today = timezone.datetime.fromisoformat(
            "2021-02-26T00:00:00.900+00:00")

        DatabaseHandler.shift_tasks(today)

        shifted = Task.objects.filter(
            init_date__date=today.date(), autoshift=True)
        self.assertEquals(shifted.count(), 1)
        shifted_task = shifted[0]
        self.assertEquals(shifted_task.title, 'test task 3')


class TestDatesHandler(TestCase):
    def test__is_end_of_month(self):
        self.assertTrue(DatesHandler.is_end_of_month(
            timezone.datetime(2020, 12, 31)))

        self.assertTrue(DatesHandler.is_end_of_month(
            timezone.datetime(2021, 2, 28)))

        self.assertTrue(DatesHandler.is_end_of_month(
            timezone.datetime(2020, 2, 29)))

        self.assertTrue(DatesHandler.is_end_of_month(
            timezone.datetime(2020, 11, 30)))

        self.assertFalse(DatesHandler.is_end_of_month(
            timezone.datetime(2020, 2, 28)))

        self.assertFalse(DatesHandler.is_end_of_month(
            timezone.datetime(2020, 12, 30)))

        self.assertFalse(DatesHandler.is_end_of_month(
            timezone.datetime(2020, 11, 29)))

        self.assertFalse(DatesHandler.is_end_of_month(
            timezone.datetime(2021, 2, 27)))
    
    def test_get_monthsdays(self):
        # CASE#1: + 1 additional week 
        monthsdays_01_2021 = [
            '2020-12-28T00:00:00+00:00', '2020-12-29T00:00:00+00:00',
            '2020-12-30T00:00:00+00:00', '2020-12-31T00:00:00+00:00',
            '2021-01-01T00:00:00+00:00', '2021-01-02T00:00:00+00:00',
            '2021-01-03T00:00:00+00:00', '2021-01-04T00:00:00+00:00',
            '2021-01-05T00:00:00+00:00', '2021-01-06T00:00:00+00:00',
            '2021-01-07T00:00:00+00:00', '2021-01-08T00:00:00+00:00',
            '2021-01-09T00:00:00+00:00', '2021-01-10T00:00:00+00:00',
            '2021-01-11T00:00:00+00:00', '2021-01-12T00:00:00+00:00',
            '2021-01-13T00:00:00+00:00', '2021-01-14T00:00:00+00:00',
            '2021-01-15T00:00:00+00:00', '2021-01-16T00:00:00+00:00',
            '2021-01-17T00:00:00+00:00', '2021-01-18T00:00:00+00:00',
            '2021-01-19T00:00:00+00:00', '2021-01-20T00:00:00+00:00',
            '2021-01-21T00:00:00+00:00', '2021-01-22T00:00:00+00:00',
            '2021-01-23T00:00:00+00:00', '2021-01-24T00:00:00+00:00',
            '2021-01-25T00:00:00+00:00', '2021-01-26T00:00:00+00:00',
            '2021-01-27T00:00:00+00:00', '2021-01-28T00:00:00+00:00',
            '2021-01-29T00:00:00+00:00', '2021-01-30T00:00:00+00:00',
            '2021-01-31T00:00:00+00:00', '2021-02-01T00:00:00+00:00',
            '2021-02-02T00:00:00+00:00', '2021-02-03T00:00:00+00:00',
            '2021-02-04T00:00:00+00:00', '2021-02-05T00:00:00+00:00',
            '2021-02-06T00:00:00+00:00', '2021-02-07T00:00:00+00:00'
        ]
        date_01_2021 = timezone.datetime.fromisoformat(
            '2021-01-01T00:00:00+00:00')
        gen_monthsdays_01_2021 = DatesHandler.get_monthdates(date_01_2021)
        self.assertEquals(monthsdays_01_2021, gen_monthsdays_01_2021)

        #CASE#2 + 2 additional weeks
        monthsdays_02_2021 = [
            '2021-02-01T00:00:00+00:00', '2021-02-02T00:00:00+00:00',
            '2021-02-03T00:00:00+00:00', '2021-02-04T00:00:00+00:00',
            '2021-02-05T00:00:00+00:00', '2021-02-06T00:00:00+00:00',
            '2021-02-07T00:00:00+00:00', '2021-02-08T00:00:00+00:00',
            '2021-02-09T00:00:00+00:00', '2021-02-10T00:00:00+00:00',
            '2021-02-11T00:00:00+00:00', '2021-02-12T00:00:00+00:00',
            '2021-02-13T00:00:00+00:00', '2021-02-14T00:00:00+00:00',
            '2021-02-15T00:00:00+00:00', '2021-02-16T00:00:00+00:00',
            '2021-02-17T00:00:00+00:00', '2021-02-18T00:00:00+00:00',
            '2021-02-19T00:00:00+00:00', '2021-02-20T00:00:00+00:00',
            '2021-02-21T00:00:00+00:00', '2021-02-22T00:00:00+00:00',
            '2021-02-23T00:00:00+00:00', '2021-02-24T00:00:00+00:00',
            '2021-02-25T00:00:00+00:00', '2021-02-26T00:00:00+00:00',
            '2021-02-27T00:00:00+00:00', '2021-02-28T00:00:00+00:00',
            '2021-03-01T00:00:00+00:00', '2021-03-02T00:00:00+00:00',
            '2021-03-03T00:00:00+00:00', '2021-03-04T00:00:00+00:00',
            '2021-03-05T00:00:00+00:00', '2021-03-06T00:00:00+00:00',
            '2021-03-07T00:00:00+00:00', '2021-03-08T00:00:00+00:00',
            '2021-03-09T00:00:00+00:00', '2021-03-10T00:00:00+00:00',
            '2021-03-11T00:00:00+00:00', '2021-03-12T00:00:00+00:00',
            '2021-03-13T00:00:00+00:00', '2021-03-14T00:00:00+00:00'
        ]
        date_02_2021 = timezone.datetime.fromisoformat(
            '2021-02-01T00:00:00+00:00')
        gen_monthsdays_02_2021 = DatesHandler.get_monthdates(date_02_2021)
        self.assertEquals(monthsdays_02_2021, gen_monthsdays_02_2021)

        # CASE#3 without additional weeks
        monthsdays_05_2021 = [
            '2021-04-26T00:00:00+00:00', '2021-04-27T00:00:00+00:00',
            '2021-04-28T00:00:00+00:00', '2021-04-29T00:00:00+00:00',
            '2021-04-30T00:00:00+00:00', '2021-05-01T00:00:00+00:00',
            '2021-05-02T00:00:00+00:00', '2021-05-03T00:00:00+00:00',
            '2021-05-04T00:00:00+00:00', '2021-05-05T00:00:00+00:00',
            '2021-05-06T00:00:00+00:00', '2021-05-07T00:00:00+00:00',
            '2021-05-08T00:00:00+00:00', '2021-05-09T00:00:00+00:00',
            '2021-05-10T00:00:00+00:00', '2021-05-11T00:00:00+00:00',
            '2021-05-12T00:00:00+00:00', '2021-05-13T00:00:00+00:00',
            '2021-05-14T00:00:00+00:00', '2021-05-15T00:00:00+00:00',
            '2021-05-16T00:00:00+00:00', '2021-05-17T00:00:00+00:00',
            '2021-05-18T00:00:00+00:00', '2021-05-19T00:00:00+00:00',
            '2021-05-20T00:00:00+00:00', '2021-05-21T00:00:00+00:00',
            '2021-05-22T00:00:00+00:00', '2021-05-23T00:00:00+00:00',
            '2021-05-24T00:00:00+00:00', '2021-05-25T00:00:00+00:00',
            '2021-05-26T00:00:00+00:00', '2021-05-27T00:00:00+00:00',
            '2021-05-28T00:00:00+00:00', '2021-05-29T00:00:00+00:00',
            '2021-05-30T00:00:00+00:00', '2021-05-31T00:00:00+00:00',
            '2021-06-01T00:00:00+00:00', '2021-06-02T00:00:00+00:00',
            '2021-06-03T00:00:00+00:00', '2021-06-04T00:00:00+00:00',
            '2021-06-05T00:00:00+00:00', '2021-06-06T00:00:00+00:00'
        ]
        date_05_2021 = timezone.datetime.fromisoformat(
            '2021-05-01T00:00:00+00:00')
        gen_monthsdays_05_2021 = DatesHandler.get_monthdates(date_05_2021)
        self.assertEquals(monthsdays_05_2021, gen_monthsdays_05_2021)