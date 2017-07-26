from __future__ import unicode_literals
from django.db import models
from ..users.models import User, UserManager
from datetime import datetime

# Create your models here.
class TripManager(models.Manager):
    def trip_validation(self, postData):
        errors = {}
        # check if the destination field is empty
        if len(postData['destination']) < 1:
            errors['destination'] = "Please enter a destination."
        # check if the description field is empty
        if len(postData['description']) < 1:
            errors['description'] = "Please enter a description."
        # check if the travel date from field is empty
        if len(str(postData['travel_from'])) < 1:
            errors['travel_from'] = "Please enter a travel date from."
        # if the travel date from field is not empty check if the date entered is before the current date
        elif str(postData['travel_from']) < str(datetime.now()):
            errors['travel_from'] = "Travel date from must be in the future."
        # check if the travel date to field is empty
        if len(str(postData['travel_to'])) < 1:
            errors['travel_to'] = "Please enter a travel to from."
        # if the travel date to field is not empty check if the date entered is before the current date
        elif str(postData['travel_to']) < str(datetime.now()):
            errors['travel_to'] = "Travel date to must be in the future."
        # if the travel to date is not before today's date check to see if the travel to date is before the travel from date
        elif postData['travel_from'] > postData['travel_to']:
            errors['travle_time'] = "Travel date to must be later than travel date from."
        return errors
class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creator = models.ForeignKey(User, related_name = "trips_creator")
    participants = models.ManyToManyField(User, related_name = "trips_participants")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
