from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def validation(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['name'] = "Please enter your name."
        elif len(postData['name']) < 3:
            errors['name'] = "First name must at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['name']):
            errors['name'] = "First name may only contain letters."
        if len(postData['username']) < 1:
            errors['username'] = "Please enter a username."
        elif len(postData['username']) < 3:
            errors['username'] = "Last name must be at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['username']):
            errors['username'] = "Last name may only contain letters."
        elif User.objects.filter(username=postData['username']):
            errors['username'] = "Username is already taken."
        if len(postData['password']) < 1:
            errors['password'] = "Please enter a password."
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        elif postData['pw_confirm'] != postData['password']:
            errors['password'] = "Passwords do not match."
        return errors
    def login_validation(self, postData):
        errors = {}
        if len(postData['username']) < 1:
            errors['loginun'] = "Please enter your username."
        elif not User.objects.filter(username=postData['username']):
            errors['loginun'] = "Incorrect username."
        if len(postData['password']) < 1:
            errors['loginpass'] = "Please enter your password."
        elif not bcrypt.checkpw(postData['password'].encode(), User.objects.get(username=postData['username']).password.encode()):
            errors['loginpass'] = "Incorrect password."
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
