import uuid
import datetime
from django.utils import timezone
from django.db import models
from decouple import config
from django.core.exceptions import ValidationError

TASK_TEMPLATE_PATH = config('TASK_TEMPLATE_PATH')

class RegisterTask(models.Model):
    """
    Register file template at particular location.
    """
    name = models.CharField(max_length=250, unique=True)
    task_file = models.FileField(upload_to=TASK_TEMPLATE_PATH, null=True)
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class RegisterJobs(models.Model):
    """
    Register Job model. Use to store job details
    """
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_name = models.CharField(max_length=250)
    scheduled_hour = models.PositiveIntegerField(null=True)
    scheduled_min = models.PositiveIntegerField(null=True)
    scheduled_date = models.DateField(null=True)
    periodic = models.BooleanField(default=False)
    CHOICES = (
        ('not_executed', 'NOT_EXCECUTED'),
        ('pending', 'PENDING'),
        ('executed', 'EXECUTED'),
        ('killed', 'KILLED')
    )
    status = models.CharField(max_length=25, choices=CHOICES, default='not_executed')
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    task_template = models.ForeignKey(RegisterTask, on_delete=models.CASCADE, related_name='registered_jobs')
