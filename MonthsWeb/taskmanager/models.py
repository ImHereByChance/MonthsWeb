from django.db import models
from django.db.models.fields import AutoField, CharField


class Task(models.Model):
    """The model, which stores the main fields of the task 
    (ID, creation date (initdate), title, description. 
    All other specific fields joins to it, such as the 
    task repetition interval or files attached to the task.
    """
    ID = models.AutoField(primary_key=True)
    initdate = models.DateTimeField(auto_now=False, auto_now_add=False)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=800, blank=True)

    def __str__(self) -> str:
        return f'id {self.ID}'


class Interval(models.Model):
    ID = models.AutoField(primary_key=True)
    interval = models.CharField(max_length=150)
    related_task = models.OneToOneField(Task, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'"{self.interval}" for task_id '\
               f'{self.related_task_id}'


class File(models.Model):
    ID = models.AutoField(primary_key=True)
    link = models.CharField(max_length=400)
    related_task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'id {self.ID} for task_id {self.related_task_id}'


class Completion(models.Model):
    ID = models.AutoField(primary_key=20)
    date_when = models.DateTimeField(auto_now=False, auto_now_add=False)
    related_task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'for the task_id {self.related_task_id} {self.date_when}'


class Autoshift(models.Model):
    ID = models.AutoField(primary_key=20)
    value = CharField(max_length=3)
    related_task = models.OneToOneField(Task, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return (f'"{self.value}" for the task_id {self.related_task.ID}')
