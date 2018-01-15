from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
import bcrypt
from .models import Trip
from ..users.models import User

def index(request):
    #if user tries to view page but has not logged in and created a request.session['id'] redirect to login and registration page with error message
    if 'id' not in request.session:
        messages.add_message(request, messages.ERROR, "You have to log in first.")
        return redirect('/')
    context = {
        #trips is set to the data stored in the Trip table where the logged in user is either the creator or a participant. Ordered by start_date
        'trips': (Trip.objects.filter(Q(creator=request.session['id']) | Q(participants=request.session['id'])).distinct()).order_by('start_date') ,
        #other_trips is set to the data stored in the Trip table where the logged in user is not the creator or a participant. Ordered by start_date
        'other_trips': (Trip.objects.exclude(Q(creator=request.session['id']) | Q(participants=request.session['id'])).distinct()).order_by('start_date')
    }
    return render(request, 'app2/app2_index.html', context)
def add(request):
    #if user tries to view page but has not logged in and created a request.session['id'] redirect to login and registration page with error message
    if 'id' not in request.session:
        messages.add_message(request, messages.ERROR, "You have to log in first.")
        return redirect('/')
    return render(request, 'app2/add.html')
def add_trip(request):
    #if there are errors add errors to messages and redirect to the 'add a trip' page
    errors = Trip.objects.trip_validation(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        # Set the values of form fields to be what user tried to enter
        context = {
            'destination_value': request.POST['destination'],
            'description_value': request.POST['description'],
            'from_value': request.POST['travel_from'],
            'to_value': request.POST['travel_to']
        }
        return render(request, 'app2/add.html', context)
    #if there are no errors then create an object in the Trip object with the entered information and link creator to the logged in user
    else:
        Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date=request.POST['travel_from'], end_date=request.POST['travel_to'], creator=User.objects.get(id=request.session['id']))
        return redirect('/travels')
def view_trip(request, number):
    #if user tries to view page but has not logged in and created a request.session['id'] redirect to login and registration page with error message
    if 'id' not in request.session:
        messages.add_message(request, messages.ERROR, "You have to log in first.")
        return redirect('/')
    #get the information for the trip where the id is the id of the trip that was clicked. Also determine if the current user is participating in the trip (either the creator or a participant)
    context = {
        'trip': Trip.objects.get(id=number),
        'participating': True if (User.objects.get(id=request.session["id"]) in Trip.objects.get(id=number).participants.all()) or (request.session["id"] == Trip.objects.get(id=number).creator.id) else False
    }
    return render(request, 'app2/view.html', context)
def join_trip(request, number, dashboard):
    # Check that the current user is not already a participant of the Trip nor the creator then add them to the list of participants for the trip
    if (User.objects.get(id=request.session["id"]) not in Trip.objects.get(id=number).participants.all()) and (request.session["id"] != Trip.objects.get(id=number).creator.id):
        Trip.objects.get(id=number).participants.add(request.session['id'])
    if dashboard == "0":
        return redirect('/travels/destination/'+number)
    return redirect('/travels')
def leave_trip(request, number, dashboard):
    # Check that the current user is not the creator of the trip and then remove them from the participants of the Trip
    if request.session["id"] != Trip.objects.get(id=number).creator.id:
        Trip.objects.get(id=number).participants.remove(request.session['id'])
    if dashboard == "0":
        return redirect('/travels/destination/'+number)
    return redirect('/travels')
def remove_user(request, trip, user):
    creator = Trip.objects.get(id=trip).creator.id
    if (request.session["id"] == creator) and (creator != user):
        Trip.objects.get(id=trip).participants.remove(user)
    return redirect('/travels/destination/'+trip)
def delete_trip(request, number):
    # Check if the current user is the creator of the trip. If so delete the Trip object
    if request.session["id"] == Trip.objects.get(id=number).creator.id:
        Trip.objects.filter(id=number).delete()
    return redirect('/travels')
