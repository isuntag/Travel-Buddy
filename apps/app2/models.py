from __future__ import unicode_literals
from django.db import models
from ..users.models import User, UserManager
from datetime import datetime

# Create your models here.
class TripManager(models.Manager):
    def trip_validation(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['destination'] = "Please enter a destination."
        if len(postData['description']) < 1:
            errors['description'] = "Please enter a description."
        if len(str(postData['travel_from'])) < 1:
            errors['travel_from'] = "Please enter a travel date from."
        elif str(postData['travel_from']) < str(datetime.now()):
            errors['travel_from'] = "Travel date from must be in the future."
        if len(str(postData['travel_to'])) < 1:
            errors['travel_to'] = "Please enter a travel to from."
        elif str(postData['travel_to']) < str(datetime.now()):
            errors['travel_to'] = "Travel date to must be in the future."
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
