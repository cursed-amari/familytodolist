from django.contrib.auth.models import User
from django.db import models


class ToDoListModel(models.Model):
    TASK_TYPE_CHOICES = [
        ('personal', 'Личный'),
        ('shared', 'Общий'),
        ('shopping', 'Список покупок'),
    ]

    title = models.CharField(max_length=128)
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    context = models.TextField(null=True, blank=True)
    complexity = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    run_time = models.DurationField(default='1 day')
    completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    task = models.ForeignKey(ToDoListModel, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    context = models.TextField(null=True, blank=True)
    complexity = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    run_time = models.DurationField(default='1 day')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TaskShare(models.Model):
    task = models.ForeignKey(ToDoListModel, related_name='shared_with', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='shared_tasks', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task', 'user')
