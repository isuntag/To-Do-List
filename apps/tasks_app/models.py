from __future__ import unicode_literals

from django.db import models

from datetime import datetime, timedelta

from ..users_app.models import User
from ..lists_app.models import List

# Create your models here.
class TaskManager(models.Manager):
    def validation(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Please enter a task."
        if postData['due_date']:
            if datetime.strptime(postData['due_date'], '%Y-%m-%d') < datetime.today()-timedelta(days=1):
                errors['due_date'] = "Invalid due date."
        return errors

class Task(models.Model):
    title = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="tasks")
    creator = models.ForeignKey(User, related_name="created_tasks", null=True)
    assignedlist = models.ForeignKey(List, related_name="tasks")
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    @property
    def is_complete(self):
        return bool(self.completed)
    objects = TaskManager()
