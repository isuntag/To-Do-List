from __future__ import unicode_literals

from django.db import models

import re

import bcrypt

from datetime import datetime, timedelta

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class UserManager(models.Manager):
    def validation(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "Please enter your first name."
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "First name must at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['first_name']):
            errors['first_name'] = "First name may only contain letters."
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Please enter your last name."
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['last_name']):
            errors['last_name'] = "Last name may only contain letters."
        if len(postData['email']) < 1:
            errors['email'] = "Please enter your email."
        elif User.objects.filter(email=postData['email']):
            errors['email'] = "Email is already taken"
        elif not re.match('[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+)*@[A-Za-z0-9-]+(.[A-Za-z0-9]+)*(.[A-Za-z]{2,})',postData['email']):
            errors['email'] = "Incorrect email format."
        if len(postData['password']) < 1:
            errors['password'] = "Please enter a password."
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        elif postData['pw_confirm'] != postData['password']:
            errors['password'] = "Passwords do not match."
        return errors
    def admin_created_user(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "Please enter your first name."
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "First name must at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['first_name']):
            errors['first_name'] = "First name may only contain letters."
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Please enter your last name."
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['last_name']):
            errors['last_name'] = "Last name may only contain letters."
        if len(postData['email']) < 1:
            errors['email'] = "Please enter your email."
        elif User.objects.filter(email=postData['email']):
            errors['email'] = "Email is already taken"
        elif not re.match('[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+)*@[A-Za-z0-9-]+(.[A-Za-z0-9]+)*(.[A-Za-z]{2,})',postData['email']):
            errors['email'] = "Incorrect email format."
        return errors
    def update_user(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "Please enter your first name."
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "First name must at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['first_name']):
            errors['first_name'] = "First name may only contain letters."
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Please enter your last name."
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['last_name']):
            errors['last_name'] = "Last name may only contain letters."
        if postData['password']:
            if len(postData['password']) < 8:
                errors['password'] = "Password must be at least 8 characters."
            elif postData['confirm_password'] != postData['password']:
                errors['password'] = "Passwords do not match."
        return errors
    def login_validation(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['loginmail'] = "Please enter your email."
        elif not User.objects.filter(email=postData['email']):
            errors['loginmail'] = "Incorrect email."
        elif len(postData['password']) < 1:
            errors['loginpass'] = "Please enter your password."
        elif not bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()):
            errors['loginpass'] = "Incorrect password."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    admin = models.BooleanField(default=0)
    company = models.ForeignKey(Company, related_name="users", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    @property
    def is_admin(self):
        return bool(self.admin)
    def __repr__(self):
        return "<Users object: {} {} {}>".format(self.first_name, self.last_name, self.email)
    objects = UserManager()

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
    # notStarted = 'not'
    # started = 'started'
    # complete = 'complete'
    # status_choices = (
    #     (notStarted, 'Not Started'),
    #     (started, 'Started'),
    #     (complete, 'Completed')
    # )
    # status = models.CharField(max_length=10, choices=status_choices, default=notStarted)
    # def is_notStarted(self):
    #     return self.status in self.notStarted
    # def is_started(self):
    #     return self.status in self.started
    # def is_complete(self):
    #     return self.status in self.complete
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    @property
    def is_complete(self):
        return bool(self.completed)
    objects = TaskManager()
