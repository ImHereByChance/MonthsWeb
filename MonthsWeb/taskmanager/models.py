from django.db import models
from django.db.models import Q
from django.db.models import Count
from django.db.models.fields import DateField
from django.db import IntegrityError


class Task(models.Model):
    """The model, which stores the main fields of the task 
    (ID, creation date (init_date), title, description,
    task repetition interval(interval), autoshift.
    All other specific fields joins to it, such as the 
    dates when task was mareked as completed or files attached to the task.
    """
    # task creation date
    init_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    # title of the task
    title = models.CharField(max_length=80)
    # description of the task
    description = models.CharField(max_length=800, blank=True)
    # task repetition interval (e.g. "every_day", "every_month" etc.)
    interval = models.CharField(max_length=150, default='no')
    # a value representing whether the task should be moved to the next date
    # if it is not completed on time 
    autoshift = models.BooleanField(default=False)
    
    class Meta:
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
                name='only_interval_or_autoshift',
            )
        ]

    def __str__(self) -> str:
        return f'id {self.id}'


class File(models.Model):
    # address to access the task
    link = models.CharField(max_length=400)
    related_task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'id {self.id} for task_id {self.related_task_id}'


class Completion(models.Model):
    # date when the related task completed
    date_completed = models.DateTimeField(auto_now=False, auto_now_add=False)
    related_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'for the task_id {self.related_task_id} {self.date_completed}'
    
    def save(self, *args, **kwargs):
        if Completion.objects\
        .filter(date_completed__date=self.date_completed)\
        .exists():
            raise IntegrityError('can be only one Completion model ',
                                 'for one Task and date')
        super(Completion, self).save(*args, **kwargs)