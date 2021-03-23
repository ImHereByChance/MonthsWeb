import datetime
from copy import deepcopy
from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from .models import Task, Completion, File
from .services.dbservice import DatabaseHandler
from .services.dateservice import DatesHandler
from .services.taskservice import TaskHandler, RepeatingTasksGenerator


class TestModels(TestCase):
    def setUp(self):
        # do not delete, only add
        task_1 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-21T16:26:03.850+00:00"),
            title='test task 1',
            description='bare task without interval and autoshift'
        )
        task_2 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-20T14:01:40.981+00:00"),
            title='test task 2',
            description='task with interval value "_every_day"',
            interval='every_week'
        )
        task_3 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-23T17:59:22.900+00:00"),
            title='test task 3',
            description='task with autoshift value True',
            autoshift=True
        )
        completion_1 = Completion.objects.create(
            date_completed=datetime.datetime.fromisoformat(
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
            slightly_different_time = datetime.datetime.fromisoformat(
                "2021-02-20T17:30:30.000+00:00"
            )
            Completion.objects.create(
                date_completed=slightly_different_time,
                related_task=existing_model.related_task
            )
        with self.assertRaises(IntegrityError):
            slightly_different_time = datetime.datetime.fromisoformat(
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
            datetime.datetime.fromisoformat(
                "2021-02-20T16:41:30.981+00:00"),
            datetime.datetime.fromisoformat(
                "2021-03-06T10:10:59.981+00:00")
        ])
        self.assertEquals(first=completion_qset.count(),
                          second=Completion.objects.none().count())


class TestDatabaseHandler(TestCase):
    def setUp(self):
        task_1 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-21T16:26:03.850+00:00"),
            title='test task 1',
            description='bare task without interval and autoshift'
        )
        task_2 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-20T14:01:40.981+00:00"),
            title='test task 2',
            description='task with interval value "_every_week"',
            interval='every_week'
        )
        task_3 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-23T17:59:22.900+00:00"),
            title='test task 3',
            description='task with autoshift value True',
            autoshift=True
        )
        task_4 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-03-01T17:59:22.900+00:00"),
            title='test task 4',
            description='task which is in next month',
        )
        task_5 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-01-01T17:59:22.900+00:00"),
            title='test task 5',
            description='with interval from previous month',
            interval='every_month'
        )
        task_6 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2026-01-01T17:59:22.900+00:00"),
            title='test task 6',
            description='far away.. just to delete',
        )
        task_7 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2028-01-01T17:59:22.900+00:00"),
            title='test task 7',
            description='far away.. just to delete',
        )
        task_8 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
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
            date_completed=datetime.datetime.fromisoformat(
                "2021-02-21T16:41:30.981+00:00"),
            related_task=task_2
        )
        completion_2 = Completion.objects.create(
            date_completed=datetime.datetime.fromisoformat(
                "2021-03-06T10:10:59.981+00:00"),
            related_task=task_2
        )
        completion_3 = Completion.objects.create(
            date_completed=datetime.datetime.fromisoformat(
                "2021-02-20T18:13:45.436+00:00"),
            related_task=task_1
        )

    def test_get_tasks_by_timerange(self):
        date_range = (
            datetime.datetime.fromisoformat(
                    "2021-02-01T00:00:00.000+00:00"),
            datetime.datetime.fromisoformat(
                    "2021-03-14T21:59:59.999+00:00")
        )

        dicts_list = DatabaseHandler.get_tasks_by_timerange(date_range)
        expected_output = [
            {'id': 10,
             'init_date': datetime.datetime(
                 2021, 2, 21, 16, 26, 3, 850000, tzinfo=datetime.timezone.utc),
             'title': 'test task 1',
             'description': 'bare task without interval and autoshift',
             'interval': 'no',
             'autoshift': False},
            {'id': 11,
             'init_date': datetime.datetime(
                 2021, 2, 20, 14, 1, 40, 981000, tzinfo=datetime.timezone.utc),
             'title': 'test task 2',
             'description': 'task with interval value "_every_week"',
             'interval': 'every_week',
             'autoshift': False},
            {'id': 12,
             'init_date': datetime.datetime(
                 2021, 2, 23, 17, 59, 22, 900000, tzinfo=datetime.timezone.utc),
             'title': 'test task 3',
             'description': 'task with autoshift value True',
             'interval': 'no',
             'autoshift': True},
            {'id': 13,
             'init_date': datetime.datetime(
                 2021, 3, 1, 17, 59, 22, 900000, tzinfo=datetime.timezone.utc),
             'title': 'test task 4',
             'description': 'task which is in next month',
             'interval': 'no',
             'autoshift': False}
        ]

        # exclude 'id' because it can vary depending on case
        dicts_list = remove_ids(dicts_list)
        expected_output = remove_ids(expected_output)
        
        self.assertEquals(first=dicts_list,
                          second=expected_output)

    def test_get_intervalled_tasks(self):
        date_range = (
            datetime.datetime.fromisoformat(
                    "2021-02-01T00:00:00.000+00:00"),
            datetime.datetime.fromisoformat(
                    "2021-03-14T21:59:59.999+00:00")
        )
        dicts_list = DatabaseHandler.get_intervalled_tasks(date_range)

        expected_output = [
            {'id': 133,
             'init_date': datetime.datetime(
                 2021, 2, 20, 14, 1, 40, 981000, tzinfo=datetime.timezone.utc),
             'title': 'test task 2',
             'description': 'task with interval value "_every_week"',
             'interval': 'every_week',
             'autoshift': False},
            {'id': 136,
             'init_date': datetime.datetime(
                 2021, 1, 1, 17, 59, 22, 900000, tzinfo=datetime.timezone.utc),
             'title': 'test task 5',
             'description': 'with interval from previous month',
             'interval': 'every_month',
             'autoshift': False}
        ]
        # exclude 'id' because it can vary depending on case
        dicts_list = remove_ids(dicts_list)
        expected_output = remove_ids(expected_output)

        self.assertEquals(dicts_list, expected_output)

    def test_get_additional_fields(self):
        date_range = (
            datetime.datetime.fromisoformat(
                "2021-02-01T00:00:00.000+00:00"),
            datetime.datetime.fromisoformat(
                "2021-03-14T21:59:59.999+00:00"),
        )

        qs = Task.objects.values_list('id').filter(
                init_date__range=date_range)
        id_set = set(i[0] for i in qs)

        additional_fields = DatabaseHandler.get_additional_fields(id_set)
        expected_output = {
            'files': [
                {'id': 1,
                 'link': 'file1/for/task/3',
                 'related_task_id': 2},
                {'id': 2,
                 'link': 'file2/for/task/3',
                 'related_task_id': 3},
            ],
            'completions': [
                {'id': 1,
                 'date_completed': datetime.datetime.fromisoformat(
                     '2021-02-21T16:41:30.981+00:00'),
                 'related_task_id': 2},
                {'id': 2,
                 'date_completed': datetime.datetime.fromisoformat(
                     "2021-03-06T10:10:59.981+00:00"),
                 'related_task_id': 2},
                {'id': 3,
                 'date_completed': datetime.datetime.fromisoformat(
                     "2021-02-20T18:13:45.436+00:00"),
                 'related_task_id': 1}
            ]
        }
        
        # get rid of any id-s
        additional_fields['files'] = remove_ids(additional_fields['files'])
        additional_fields['completions'] = remove_ids(
                additional_fields['completions'])
        expected_output['files'] = remove_ids(additional_fields['files'])
        expected_output['completions'] = remove_ids(
                additional_fields['completions'])

        self.assertEquals(first=additional_fields,
                          second=expected_output)

    def test_create_task_and_related(self):
        """task_dict_with_related simulates a dict with the fields of
        model Task and models related to it, which came from client.
        From the field of task_dict_with_related should be created Task
        and models related to it: Completion and File(can be many).
        """
        # task dict with fields from related models as it comes form client 
        task_dict_with_related = {
            'id': None,
            'date': "2021-02-01T00:00:00+00:00",
            'init_date': "2021-02-01T00:00:00+00:00",
            'title': 'task created for test_create_task_and_related()',
            'description': 'with 2 files',
            'interval': 'no',
            'autoshift': False,
            'completion': False,
            'files': [
                {'id': None,
                 'link': 'file_1/for/created_Task',
                 'related_task_id': None},
                {'id': None,
                 'link': 'file_2/for/created_Task',
                 'related_task_id': None} 
            ]
        }
        # process of creation
        DatabaseHandler.create_task_and_related(task_dict_with_related)
        
        created_Task = Task.objects\
            .get(title='task created for test_create_task_and_related()')

        # is there the Task with our title and date there? 
        self.assertEquals(
            first=(created_Task.title,
                   created_Task.init_date.isoformat()),
            second=(task_dict_with_related['title'],
                    task_dict_with_related['init_date']))
            
        # are there two File models related to created_Task?
        try:
            File.objects.get(
                    related_task=created_Task,
                    link='file_1/for/created_Task')
            File.objects.get(
                    related_task=created_Task,
                    link='file_2/for/created_Task')
        except Exception as err:
            self.fail(str(err))

    def test_update_task_and_related(self):
        # CASE#1 without attached files
        task_1 = Task.objects.get(title='test task 1')
        expected_output_1 = {
            'id': task_1.id,
            'date': '2021-02-16T00:00:00.000+00:00',
            'init_date': '2021-02-16T00:00:00.000+00:00',
            'title': 'updateted task#1',
            'description': '+interval',
            'interval': 'every_month',
            'autoshift': False
        }
        DatabaseHandler.update_task_and_related(expected_output_1)
        updated_dict = Task.objects.values().filter(id=task_1.id)[0]

        del expected_output_1['date']
        expected_output_1['init_date'] = datetime.datetime.fromisoformat(
                                               expected_output_1['init_date'])

        self.assertEquals(expected_output_1, updated_dict)


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
        task_completion = datetime.datetime.fromisoformat(
            '2021-03-01T19:53:22.900+00:00')
        task_dict = {
            'id': task_id,
            'completion': '2021-03-01T19:53:22.900+00:00',
            'date': '2021-03-01T17:59:22.900+00:00'
        }

        DatabaseHandler.check_uncheck_task(task_dict)
        created = Completion.objects.get(related_task_id=task_id,
                                         date_completed=task_completion)

        self.assertEquals(created.related_task_id, task_id)

        # CASE#2: must delete the previous
        task_dict['completion'] = False
        DatabaseHandler.check_uncheck_task(task_dict)
        test_query = Completion.objects.filter(related_task_id=task_id,
                                               date_completed=task_completion)
        self.assertFalse(test_query)

        # CASE#3: intervalled task
        task = Task.objects.get(title='test task 2')
        task_completion = datetime.datetime.fromisoformat(
            "2021-02-27T14:01:40.981+00:00")
        task_dict = {
            'id': task.id,
            'completion': "2021-02-27T14:01:40.981+00:00",
            'date': '2021-02-20T00:00:00.000+00:00'
        }

        DatabaseHandler.check_uncheck_task(task_dict)
        created = Completion.objects.get(related_task_id=task.id,
                                         date_completed=task_completion)

        self.assertEquals(created.related_task_id, task.id)

    def test_shift_tasks(self):
        today = datetime.datetime.fromisoformat(
            "2021-02-26T00:00:00.900+00:00")

        DatabaseHandler.shift_tasks(today)

        shifted = Task.objects.filter(
            init_date__date=today.date(), autoshift=True)
        self.assertEquals(shifted.count(), 1)
        shifted_task = shifted[0]
        self.assertEquals(shifted_task.title, 'test task 3')


class TestDatesHandler(TestCase):
    def test_is_end_of_month(self):
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
        date_01_2021 = datetime.datetime.fromisoformat(
            '2021-01-01T00:00:00+00:00')
        gen_monthsdays_01_2021 = DatesHandler.generate_month_dates(date_01_2021)
        self.assertEquals(monthsdays_01_2021, gen_monthsdays_01_2021)

        # CASE#2 + 2 additional weeks
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
        date_02_2021 = datetime.datetime.fromisoformat(
            '2021-02-01T00:00:00+00:00')
        gen_monthsdays_02_2021 = DatesHandler.generate_month_dates(date_02_2021)
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
        date_05_2021 = datetime.datetime.fromisoformat(
            '2021-05-01T00:00:00+00:00')
        gen_monthsdays_05_2021 = DatesHandler.generate_month_dates(date_05_2021)
        self.assertEquals(monthsdays_05_2021, gen_monthsdays_05_2021)


class TestRepeatingTasksGenerator(TestCase):
    def setUp(self):
        task_1 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-21T00:00:00.000000+00:00"),
            title='test task 1',
            description='bare task without interval and autoshift'
        )
        task_2 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-20T00:00:00.000000+00:00"),
            title='test task 2',
            description='task with interval value "_every_week"',
            interval='every_week'
        )
        task_3 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-23T00:00:00.000000+00:00"),
            title='test task 3',
            description='task with interval "_every_workday"',
            interval='every_workday'
        )
        task_4 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-03-02T00:00:00.000000+00:00"),
            title='test task 4',
            description='task which is in next month',
        )
        task_5 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-01-01T00:00:00.000000+00:00"),
            title='test task 5',
            description='with interval from previous month',
            interval='every_month'
        )

    def test_every_day(self):
        # date when task was initialized
        init_date = timezone.datetime(2020, 10, 4)

        self.assertTrue(RepeatingTasksGenerator._every_day(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 5))
        )
        self.assertTrue(RepeatingTasksGenerator._every_day(
            init_date=init_date,
            checkdate=timezone.datetime(2048, 5, 27))
        )
        self.assertFalse(RepeatingTasksGenerator._every_day(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 4))
        )
        self.assertFalse(RepeatingTasksGenerator._every_day(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 3))
        )
        self.assertFalse(RepeatingTasksGenerator._every_day(
            init_date=init_date,
            checkdate=timezone.datetime(2007, 10, 3))
        )

    def test_every_workday(self):
        # date when task was initialized (Monday)
        init_date = timezone.datetime(2020, 10, 5)

        self.assertTrue(RepeatingTasksGenerator._every_workday(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 6))
        )
        self.assertTrue(RepeatingTasksGenerator._every_workday(
            init_date=init_date,
            checkdate=timezone.datetime(2050, 4, 4))
        )
        self.assertTrue(RepeatingTasksGenerator._every_workday(
            init_date=timezone.datetime(2020, 6, 28),
            checkdate=timezone.datetime(2021, 1, 13))
        )
        self.assertFalse(RepeatingTasksGenerator._every_workday(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 5))
        )
        self.assertFalse(RepeatingTasksGenerator._every_workday(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 4))
        )
        self.assertFalse(RepeatingTasksGenerator._every_workday(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 2))
        )
        self.assertFalse(RepeatingTasksGenerator._every_workday(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 10))
        )

    def test_every_week(self):
        # date when task was initialized (Monday)
        init_date = timezone.datetime(2020, 10, 5)

        self.assertTrue(RepeatingTasksGenerator._every_week(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 12, 14))
        )
        self.assertTrue(RepeatingTasksGenerator._every_week(
            init_date=init_date,
            checkdate=timezone.datetime(2050, 4, 4))
        )
        self.assertFalse(RepeatingTasksGenerator._every_week(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 5))
        )
        self.assertFalse(RepeatingTasksGenerator._every_week(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 21))
        )
        self.assertFalse(RepeatingTasksGenerator._every_week(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 11, 22))
        )

    def test_month(self):
        # date when task was initialized (Monday)
        init_date = timezone.datetime(2020, 10, 5)

        self.assertTrue(RepeatingTasksGenerator._every_month(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 11, 5))
        )
        self.assertTrue(RepeatingTasksGenerator._every_month(
            init_date=init_date,
            checkdate=timezone.datetime(2023, 2, 5))
        )
        self.assertTrue(RepeatingTasksGenerator._every_month(
            init_date=timezone.datetime(2020, 10, 31),
            checkdate=timezone.datetime(2020, 11, 30))
        )
        self.assertTrue(RepeatingTasksGenerator._every_month(
            init_date=timezone.datetime(2020, 10, 31),
            checkdate=timezone.datetime(2021, 2, 28))
        )
        self.assertTrue(RepeatingTasksGenerator._every_month(
            init_date=timezone.datetime(2020, 1, 30),
            checkdate=timezone.datetime(2020, 2, 29))
        )
        self.assertTrue(RepeatingTasksGenerator._every_month(
            init_date=timezone.datetime(2020, 2, 29),
            checkdate=timezone.datetime(2021, 1, 29))
        )
        self.assertTrue(RepeatingTasksGenerator._every_month(
            init_date=timezone.datetime(2020, 2, 29),
            checkdate=timezone.datetime(2021, 2, 28))
        )
        self.assertTrue(RepeatingTasksGenerator._every_month(
            init_date=timezone.datetime(2020, 10, 30),
            checkdate=timezone.datetime(2021, 2, 28))
        )
        self.assertFalse(RepeatingTasksGenerator._every_month(
            init_date=init_date,
            checkdate=init_date)
        )
        self.assertFalse(RepeatingTasksGenerator._every_month(
            init_date=init_date,
            checkdate=timezone.datetime(2020, 10, 6))
        )
        self.assertFalse(RepeatingTasksGenerator._every_month(
            init_date=init_date,
            checkdate=timezone.datetime(2019, 9, 5))
        )
        self.assertFalse(RepeatingTasksGenerator._every_month(
            init_date=timezone.datetime(2020, 10, 30),
            checkdate=timezone.datetime(2021, 2, 27))
        )
        self.assertFalse(RepeatingTasksGenerator._every_month(
            init_date=timezone.datetime(2020, 1, 29),
            checkdate=timezone.datetime(2021, 4, 28))
        )
        self.assertTrue(RepeatingTasksGenerator._every_month(
            init_date=timezone.datetime(2020, 1, 29),
            checkdate=timezone.datetime(2021, 4, 29))
        )
        self.assertFalse(RepeatingTasksGenerator._every_month(
            init_date=timezone.datetime(2020, 1, 29),
            checkdate=timezone.datetime(2021, 4, 30))
        )

    def test_every_year(self):
        # date when task was initialized (Monday)
        init_date = timezone.datetime(2020, 10, 5)

        self.assertTrue(RepeatingTasksGenerator._every_year(
            init_date=init_date,
            checkdate=timezone.datetime(2021, 10, 5))
        )
        self.assertTrue(RepeatingTasksGenerator._every_year(
            init_date=init_date,
            checkdate=timezone.datetime(2050, 10, 5))
        )
        self.assertTrue(RepeatingTasksGenerator._every_year(
            init_date=timezone.datetime(2020, 2, 29),
            checkdate=timezone.datetime(2021, 2, 28))
        )
        self.assertTrue(RepeatingTasksGenerator._every_year(
            init_date=timezone.datetime(2020, 2, 29),
            checkdate=timezone.datetime(2024, 2, 29))
        )
        self.assertFalse(RepeatingTasksGenerator._every_year(
            init_date=timezone.datetime(2020, 2, 27),
            checkdate=timezone.datetime(2021, 2, 28))
        )
        self.assertFalse(RepeatingTasksGenerator._every_year(
            init_date=init_date,
            checkdate=init_date)
        )
        self.assertFalse(RepeatingTasksGenerator._every_year(
            init_date=timezone.datetime(2020, 2, 27),
            checkdate=timezone.datetime(2021, 2, 28))
        )
        self.assertFalse(RepeatingTasksGenerator._every_year(
            init_date=timezone.datetime(2020, 2, 27),
            checkdate=timezone.datetime(2019, 2, 27))
        )
        self.assertFalse(RepeatingTasksGenerator._every_year(
            init_date=timezone.datetime(2020, 2, 29),
            checkdate=timezone.datetime(2024, 2, 28))
        )

    def test_generate(self):
        # self.maxDiff = None
        testing_date = datetime.datetime.fromisoformat(
            '2021-02-01T00:00:00+00:00')
        datetime_objects = DatesHandler.generate_month_dates(testing_date,
                                                       as_objects=True)
        date_range = datetime_objects[0], datetime_objects[-1]
        intervalled_tasks = DatabaseHandler.get_intervalled_tasks(date_range)
        # import pdb; pdb.set_trace()
        repeated = RepeatingTasksGenerator.generate(datetime_objects,
                                                       intervalled_tasks)
        expected_output = [
            {'id': 136,
            'init_date': datetime.datetime(
                2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 5',
            'description': 'with interval from previous month',
            'interval': 'every_month',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 2, 1, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 2, 24, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 2, 25, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 2, 26, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 133,
            'init_date': datetime.datetime(
                2021, 2, 20, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 2, 27, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 1, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 136,
            'init_date': datetime.datetime(
                2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 5',
            'description': 'with interval from previous month',
            'interval': 'every_month',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 1, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 2, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 3, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 4, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 5, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 133,
            'init_date': datetime.datetime(
                2021, 2, 20, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 6, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 8, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 9, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 10, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 11, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 2, 23, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 3',
            'description': 'task with interval "_every_workday"',
            'interval': 'every_workday',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 12, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 133,
            'init_date': datetime.datetime(
                2021, 2, 20, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 13, 0, 0, tzinfo=datetime.timezone.utc)}
        ]
        
        # get rid of ids and unify the datetimes
        for ls in (repeated, expected_output):
            for d in ls:
                try:
                    del d['id']
                    d['date'] = d['date'].isoformat()
                    d['init_date'] = d['init_date'].isoformat()
                except KeyError:
                    continue
    
        self.assertEquals(first=repeated, second=expected_output)


class TestTaskHandler(TestCase):
    def setUp(self):
        task_1 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-21T00:00:00.000000+00:00"),
            title='test task 1',
            description='bare task without interval and autoshift'
        )
        task_2 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-02-20T00:00:00.000000+00:00"),
            title='test task 2',
            description='task with interval value "_every_week"',
            interval='every_week'
        )
        task_4 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-03-02T00:00:00.000000+00:00"),
            title='test task 4',
            description='task which is in next month',
        )
        task_5 = Task.objects.create(
            init_date=datetime.datetime.fromisoformat(
                "2021-01-01T00:00:00.000000+00:00"),
            title='test task 5',
            description='with interval from previous month',
            interval='every_month'
        )
        
        completion1 = Completion.objects.create(
            date_completed=datetime.datetime(
                2021, 2, 1, 0, 0, tzinfo=datetime.timezone.utc),
            related_task=task_5
        )
        completion2 = Completion.objects.create(
            date_completed=datetime.datetime(
                2021, 3, 1, 0, 0, tzinfo=datetime.timezone.utc),
            related_task=task_5
        )
        completion3 = Completion.objects.create(
            date_completed=datetime.datetime(
                2021, 3, 13, 0, 0, tzinfo=datetime.timezone.utc),
            related_task=task_2
        )
        
        file1 = File.objects.create(
            link='file1/for/task2',
            related_task=task_2
        )
        file2 = File.objects.create(
            link='file2/for/task5',
            related_task=task_5
        )
        file3 = File.objects.create(
            link='file3/for/task5',
            related_task=task_5
        )
        
        # common 
        testing_date = datetime.datetime.fromisoformat(
            '2021-02-01T00:00:00+00:00')
        datetime_objects = DatesHandler.generate_month_dates(testing_date,
                                                            as_objects=True)
        date_range = datetime_objects[0], datetime_objects[-1]
        
        self.task_handler = TaskHandler(db_service=DatabaseHandler)

        # for test_get_intervalled_tasks_dicts()
        self.intervalled_tasks_dicts = self.task_handler\
            ._get_tasks_by_intervall(datetime_objects=datetime_objects
        )
        # for test_get_tasks_by_timerange_dicts()
        self.monthly_tasks_dicts = self.task_handler\
            ._get_tasks_by_month(date_range)
        
        # for test_add_remain_fields()
        task_dicts = (deepcopy(self.monthly_tasks_dicts) +
                      deepcopy(self.intervalled_tasks_dicts))
        self.remain_fields = self.task_handler._add_remain_fields(task_dicts)

    def test_get_intervalled_tasks_dicts(self):
        
        expected_output = [
            {'id': 136,
            'init_date': datetime.datetime(
                2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 5',
            'description': 'with interval from previous month',
            'interval': 'every_month',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 2, 1, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 133,
            'init_date': datetime.datetime(
                2021, 2, 20, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 2, 27, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 136,
            'init_date': datetime.datetime(
                2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 5',
            'description': 'with interval from previous month',
            'interval': 'every_month',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 1, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 133,
            'init_date': datetime.datetime(
                2021, 2, 20, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 6, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 133,
            'init_date': datetime.datetime(
                2021, 2, 20, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 13, 0, 0, tzinfo=datetime.timezone.utc)}
            ]

        # without id-s
        self.intervalled_tasks_dicts = [
            {k:v for k,v in dct.items() if k != 'id'}
            for dct in self.intervalled_tasks_dicts
        ]
        expected_output = [
            {k:v for k,v in dct.items() if k != 'id'} 
            for dct in expected_output
        ]
        self.assertEquals(expected_output, self.intervalled_tasks_dicts)

    def test_get_tasks_by_timerange_dicts(self): 
        self.maxDiff = None
        expected_output = [
            {'id': 132,
            'init_date': datetime.datetime(
                2021, 2, 21, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 1',
            'description': 'bare task without interval and autoshift',
            'interval': 'no',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 2, 21, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 133,
            'init_date': datetime.datetime(
                2021, 2, 20, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 2, 20, 0, 0, tzinfo=datetime.timezone.utc)},
            {'id': 134,
            'init_date': datetime.datetime(
                2021, 3, 2, 0, 0, tzinfo=datetime.timezone.utc),
            'title': 'test task 4',
            'description': 'task which is in next month',
            'interval': 'no',
            'autoshift': False,
            'date': datetime.datetime(
                2021, 3, 2, 0, 0, tzinfo=datetime.timezone.utc)}
        ]
        # without id-s
        self.monthly_tasks_dicts = [
            {k:v for k,v in dct.items() if k != 'id'}
            for dct in self.monthly_tasks_dicts
        ]
        expected_output = [
            {k:v for k,v in dct.items() if k != 'id'} 
            for dct in expected_output
        ]
        self.assertEquals(expected_output, self.monthly_tasks_dicts)

    def test_add_remain_fields(self):
        expected_output = [
            {'init_date':  datetime.datetime.fromisoformat(
                                '2021-02-21T00:00:00+00:00'),
            'title': 'test task 1',
            'description': 'bare task without interval and autoshift',
            'interval': 'no',
            'autoshift': False,
            'date':  datetime.datetime.fromisoformat(
                                '2021-02-21T00:00:00+00:00'),
            'files': [],
            'completion': False},
            {'init_date':  datetime.datetime.fromisoformat(
                                '2021-02-20T00:00:00+00:00'),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date':  datetime.datetime.fromisoformat(
                                '2021-02-20T00:00:00+00:00'),
            'files': [
                {'id': 17, 'link': 'file1/for/task2', 'related_task_id': 107}
            ],
            'completion': False},
            {'init_date':  datetime.datetime.fromisoformat(
                                '2021-03-02T00:00:00+00:00'),
            'title': 'test task 4',
            'description': 'task which is in next month',
            'interval': 'no',
            'autoshift': False,
            'date':  datetime.datetime.fromisoformat(
                                '2021-03-02T00:00:00+00:00'),
            'files': [],
            'completion': False},
            {'init_date':  datetime.datetime.fromisoformat(
                                '2021-01-01T00:00:00+00:00'),
            'title': 'test task 5',
            'description': 'with interval from previous month',
            'interval': 'every_month',
            'autoshift': False,
            'date':  datetime.datetime.fromisoformat(
                                '2021-02-01T00:00:00+00:00'),
            'files': [
                {'id': 18, 'link': 'file2/for/task5', 'related_task_id': 109},
                {'id': 19, 'link': 'file3/for/task5', 'related_task_id': 109}
            ],
            'completion': datetime.datetime.fromisoformat(
                                '2021-02-01T00:00:00+00:00')},
            {'init_date':  datetime.datetime.fromisoformat(
                                '2021-02-20T00:00:00+00:00'),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date':  datetime.datetime.fromisoformat(
                                '2021-02-27T00:00:00+00:00'),
            'files': [
                {'id': 17, 'link': 'file1/for/task2', 'related_task_id': 107}
            ],
            'completion': False},
            {'init_date':  datetime.datetime.fromisoformat(
                                '2021-01-01T00:00:00+00:00'),
            'title': 'test task 5',
            'description': 'with interval from previous month',
            'interval': 'every_month',
            'autoshift': False,
            'date':  datetime.datetime.fromisoformat(
                                '2021-03-01T00:00:00+00:00'),
            'files': [
                {'id': 18, 'link': 'file2/for/task5', 'related_task_id': 109},
                {'id': 19, 'link': 'file3/for/task5', 'related_task_id': 109}
            ],
            'completion': datetime.datetime.fromisoformat(
                                '2021-03-01T00:00:00+00:00')},
            {'init_date':  datetime.datetime.fromisoformat(
                                '2021-02-20T00:00:00+00:00'),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date':  datetime.datetime.fromisoformat(
                                '2021-03-06T00:00:00+00:00'),
            'files': [
                {'id': 17, 'link': 'file1/for/task2', 'related_task_id': 107}
            ],
            'completion': False},
            {'init_date':  datetime.datetime.fromisoformat(
                                '2021-02-20T00:00:00+00:00'),
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date':  datetime.datetime.fromisoformat(
                                '2021-03-13T00:00:00+00:00'),
            'files': [
                {'id': 17, 'link': 'file1/for/task2', 'related_task_id': 107}
            ],
            'completion': datetime.datetime.fromisoformat(
                                '2021-03-13T00:00:00+00:00')}
        ]
        
        # without id-s and dates objects converted to iso string 
        self.remain_fields = [
            {k:v for k,v in dct.items() if k != 'id'}
            for dct in self.remain_fields
        ]
        expected_output = [
            {k:v for k,v in dct.items() if k != 'id'} 
            for dct in expected_output
        ]
        copy_ramain_fields = deepcopy(self.remain_fields)
        copy_expected_output = deepcopy(expected_output)
        for l in copy_ramain_fields, copy_expected_output:
            for d in l:
                d['init_date'] = d['init_date'].isoformat()
                d['date'] = d['date'].isoformat()
                if d['completion']:
                    d['completion'] = d['completion'].isoformat()
                d['files'] = [
                    {k:v for k,v in file_dict.items()
                     if k not in ['id', 'related_task_id']}
                    for file_dict in d['files']
                ]
        self.assertEquals(copy_ramain_fields, copy_expected_output)
  
    def test_convert_dates_to_strings(self):
        expected_output = [
            {'init_date': '2021-02-21T00:00:00+00:00',
            'title': 'test task 1',
            'description': 'bare task without interval and autoshift',
            'interval': 'no',
            'autoshift': False,
            'date': '2021-02-21T00:00:00+00:00',
            'files': [],
            'completion': False},
            {'init_date': '2021-02-20T00:00:00+00:00',
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': '2021-02-20T00:00:00+00:00',
            'files': [
                {'id': 17, 'link': 'file1/for/task2', 'related_task_id': 107}
            ],
            'completion': False},
            {'init_date': '2021-03-02T00:00:00+00:00',
            'title': 'test task 4',
            'description': 'task which is in next month',
            'interval': 'no',
            'autoshift': False,
            'date': '2021-03-02T00:00:00+00:00',
            'files': [],
            'completion': False},
            {'init_date': '2021-01-01T00:00:00+00:00',
            'title': 'test task 5',
            'description': 'with interval from previous month',
            'interval': 'every_month',
            'autoshift': False,
            'date': '2021-02-01T00:00:00+00:00',
            'files': [
                {'id': 18, 'link': 'file2/for/task5', 'related_task_id': 109},
                {'id': 19, 'link': 'file3/for/task5', 'related_task_id': 109}
            ],
            'completion': '2021-02-01T00:00:00+00:00'},
            {'init_date': '2021-02-20T00:00:00+00:00',
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': '2021-02-27T00:00:00+00:00',
            'files': [
                {'id': 17, 'link': 'file1/for/task2', 'related_task_id': 107}
            ],
            'completion': False},
            {'init_date': '2021-01-01T00:00:00+00:00',
            'title': 'test task 5',
            'description': 'with interval from previous month',
            'interval': 'every_month',
            'autoshift': False,
            'date': '2021-03-01T00:00:00+00:00',
            'files': [
                {'id': 18, 'link': 'file2/for/task5', 'related_task_id': 109},
                {'id': 19, 'link': 'file3/for/task5', 'related_task_id': 109}
            ],
            'completion': '2021-03-01T00:00:00+00:00'},
            {'init_date': '2021-02-20T00:00:00+00:00',
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': '2021-03-06T00:00:00+00:00',
            'files': [
                {'id': 17, 'link': 'file1/for/task2', 'related_task_id': 107}
            ],
            'completion': False},
            {'init_date': '2021-02-20T00:00:00+00:00',
            'title': 'test task 2',
            'description': 'task with interval value "_every_week"',
            'interval': 'every_week',
            'autoshift': False,
            'date': '2021-03-13T00:00:00+00:00',
            'files': [
                {'id': 17, 'link': 'file1/for/task2', 'related_task_id': 107}
            ],
            'completion': '2021-03-13T00:00:00+00:00'}
        ]
        eventual = self.task_handler._convert_dates_to_strings(self.remain_fields)
        #  without id-s
        for lst in (eventual, expected_output):
            remove_ids(lst)
        self.assertEquals(eventual, expected_output)


def remove_ids(dicts_list: list) -> list:
    """Remove (recursively) keys with names 'id' and 'related_task_id'
    from all dicts in `dicts_list`
    """
    for d in dicts_list:
        to_delete = []
        for key, value in d.items():    
            # recursive purge nested containers
            if type(value) in [list, tuple, set]:
                remove_ids(value)
            elif key in ['id', 'related_task_id']:
                to_delete.append(key)
        for k in to_delete:
            del d[k]
    
    return dicts_list
