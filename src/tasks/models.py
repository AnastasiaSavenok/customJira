import uuid
from django.db import models

from src.users.models import CustomUser


class TaskStatus(models.TextChoices):
    AWAITS_PERFORMER = 'awaits_performer'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.AWAITS_PERFORMER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_tasks',
                                 limit_choices_to={'user_type': 'customer'})
    employee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='employee_tasks',
                                 limit_choices_to={'user_type': 'employee'})
    report = models.CharField(max_length=255, blank=True, null=True)
