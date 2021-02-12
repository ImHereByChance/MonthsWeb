from django.db import models
from django.db.models.fields import AutoField, CharField


class Task(models.Model):
    ID = models.AutoField(primary_key=True)
    initdate = models.CharField(max_length=50)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=800, blank=True)

    def __str__(self) -> str:
        return f'"{self.title}", id: {self.ID}'


class Interval(models.Model):
    ID = models.AutoField(primary_key=True)
    interval = models.CharField(max_length=150)
    related_task = models.OneToOneField(Task, on_delete=models.CASCADE)

    @property
    def task_id(self):
        return self.related_task.ID

    def __str__(self) -> str:
        return f"""interval "{self.interval}" 
                   for the task: <{self.related_task.ID}>"""


class File(models.Model):
    ID = models.AutoField(primary_key=True)
    link = models.CharField(max_length=400)
    related_task = models.OneToOneField(Task, on_delete=models.CASCADE)

    @property
    def task_id(self):
        return self.related_task.ID

    def __str__(self) -> str:
        return f"""interval "{self.interval}" 
                   for the task: <{self.related_task.ID}>"""


class Completion(models.Model):
    ID = models.AutoField(primary_key=20)
    date_when = CharField(max_length=20)
    related_task = models.OneToOneField(Task, on_delete=models.CASCADE)

    @property
    def task_id(self):
        return self.related_task.ID

    def __str__(self) -> str:
        return f"""interval "{self.interval}" 
                   for the task: <{self.related_task.ID}>"""


class Autoshift(models.Model):
    ID = models.AutoField(primary_key=20)
    value = CharField(max_length=1)
    related_task = models.OneToOneField(Task, on_delete=models.CASCADE)

    @property
    def task_id(self):
        return self.related_task.ID

    def __str__(self) -> str:
        return f"""interval "{self.interval}" 
                   for the task: <{self.related_task.ID}>"""
