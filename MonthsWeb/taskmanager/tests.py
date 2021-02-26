from typing import overload
from django.test import TestCase
from django.db.models.fields import CharField
from django.db.models.functions import Cast
from django.utils import timezone
from django.db import IntegrityError
from .models import (Task, Completion, File)
from .services.dbservice import Database_handler


class TestModels(TestCase):
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

    def test_task_creation_constraint(self):
        with self.assertRaises(IntegrityError):
            Task.objects.create(init_date=timezone.now(),
                                title='nevermind',
                                interval='every_day',
                                autoshift=True)

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


class TestDatabase_handler(TestCase):
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
            title='test task 4',
            description='with interval from previous month',
            interval='every_month'
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

        tuples_list = Database_handler.get_monthly_tasks(dates_period)

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

        tuples_list = Database_handler.get_intervalled_tasks(dates_period)

        expected_output = [
            ('every_week', 133, '2021-02-20 14:01:40.981+00', 'test task 2',
             'task with interval value "every_week"', False),

            ('every_month', 136, '2021-01-01 17:59:22.9+00', 'test task 4',
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

        qs = Task.objects.values_list('id').filter(init_date__range=dates_period)
        id_set = set(i[0] for i in qs)

        tuples_list = Database_handler.get_additional_fields(id_set)

        expected_output = [
            (10, None, None, None, None),
            (8, '2021-03-06 10:10:59.981+00', None, None, None),
            (9, None, 4, 'file2/for/task/3', 9),
            (9, None, 3, 'file1/for/task/3', 9),
            (7, '2021-02-20 18:13:45.436+00', None, None, None),
            (8, '2021-02-21 16:41:30.981+00', None, None, None)
        ]
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
        Database_handler.add_overall_task(task1_dict)
        
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
        Database_handler.update_overall_task(expected_output)
        updated_dict = Task.objects.values().filter(id=task.id)[0]
        
        del expected_output['date']
        expected_output['init_date'] = timezone.datetime.fromisoformat(
            expected_output['init_date']
        )

        self.assertEquals(expected_output, updated_dict)


