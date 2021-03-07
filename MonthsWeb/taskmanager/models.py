from django.db import models
from django.db.models import Q
from django.db import IntegrityError


class Task(models.Model):
    """A model containing basic information about a user-created task.
    This information is represented by the following fields:
    1) id;
    2) init_date (task creation date);
    3) title (title of the task);
    4) description (description of the task);
    5) interval (when to repeat the task, e.g. "__every_day",
    "_every_month" etc.);
    6) autoshift (a value indicating whether the task should be
    rescheduled to the next date if it was not completed on time);

    Task has related models that store additional information about it:
    1) File (attaced to the Task, such as text document, spreadsheat, etc.)
    2) Completion (date, when user marked the task as completed)
    """
    # task creation date
    init_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    # title of the task
    title = models.CharField(max_length=80)
    # description of the task
    description = models.CharField(max_length=800, blank=True)
    # task repetition interval (e.g. "__every_day", "_every_month" etc.)
    interval = models.CharField(max_length=150, default='no')
    # a value indicating whether the task should be rescheduled to the
    # next date if it was not completed on time (shifted if not completed)
    autoshift = models.BooleanField(default=False)
    
    class Meta:
        # model should hold interval or autoshift (or none of them) - not both.
        constraints = [
            models.CheckConstraint(
                check=(
                    ~Q(interval='no') & 
                    Q(autoshift=False)
                ) | (
                    Q(interval='no') & 
                    Q(autoshift=True)
                ) | (
                    Q(interval='no') &
                    Q(autoshift=False)
                ),
                name='interval_or_autoshift',
            )
        ]

    def __str__(self) -> str:
        return f'id {self.id}'


class File(models.Model):
    """ File, attached to the user-created task (text document,
    spreadsheat, etc.). File represented as a link to the place
    where the task stored.
    
    """
    # address to access the task
    link = models.CharField(max_length=400)
    # task to which the file is attached
    related_task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'id {self.id} for task_id {self.related_task_id}'


class Completion(models.Model):
    """ Date when a user marked the task as completed."""
    # date when the related task completed
    date_completed = models.DateTimeField(auto_now=False, auto_now_add=False)
    # completed task
    related_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'for the task_id {self.related_task_id} {self.date_completed}'
    
    def save(self, *args, **kwargs):
        if Completion.objects\
        .filter(date_completed__date=self.date_completed)\
        .exists():
            raise IntegrityError(
                        'Completion must be unique for one Task and one date')
        
        super(Completion, self).save(*args, **kwargs)
