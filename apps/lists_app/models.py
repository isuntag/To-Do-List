from __future__ import unicode_literals

from django.db import models
from ..users_app.models import User

# Create your models here.
class ListManager(models.Manager):
    def validation(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Please enter a title."
        return errors

class List(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, related_name="created_lists", null=True)
    users = models.ManyToManyField(User, related_name="lists")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ListManager()
