from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def validation(self, postData):
        #validation checks for registration form
        errors = {}
        #check if name field is empty
        if len(postData['name']) < 1:
            errors['name'] = "Please enter your name."
        #if name field isn't empty check if name entered is less than 3 characters
        elif len(postData['name']) < 3:
            errors['name'] = "First name must at least 2 characters."
        #if name entered is 3 or more characters check if it only contains letters
        elif not re.match('[A-Za-z]+', postData['name']):
            errors['name'] = "First name may only contain letters."
        #check is username field is empty
        if len(postData['username']) < 1:
            errors['username'] = "Please enter a username."
        #if username field isn't empty check if username entered is less than 3 characters
        elif len(postData['username']) < 3:
            errors['username'] = "Last name must be at least 2 characters."
        #if username entered is 3 or more characters check if it only contains letters
        elif not re.match('[A-Za-z]+', postData['username']):
            errors['username'] = "Last name may only contain letters."
        #if username only contains letters check if it is already in the database
        elif User.objects.filter(username=postData['username']):
            errors['username'] = "Username is already taken."
        #check if password field is empty
        if len(postData['password']) < 1:
            errors['password'] = "Please enter a password."
        #if password field isn't empty check if password entered is less than 8 characters
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        #if password entered is 8 characters or more check if the confirm password entered is not the same as the password entered
        elif postData['pw_confirm'] != postData['password']:
            errors['password'] = "Passwords do not match."
        return errors
    def login_validation(self, postData):
        #validation for login form
        errors = {}
        #check if username field is empty
        if len(postData['username']) < 1:
            errors['loginun'] = "Please enter your username."
        #if username field is not empty check to see if username entered isn't in the database
        elif not User.objects.filter(username=postData['username']):
            errors['loginun'] = "Incorrect username."
        #check if password field is empty
        if len(postData['password']) < 1:
            errors['loginpass'] = "Please enter your password."
        #if password field is not empty check to see if it doesn't matched the stored password for the user with the entered username
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
