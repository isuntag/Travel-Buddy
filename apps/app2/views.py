from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
import bcrypt
from .models import Trip
from ..users.models import User

def index(request):
    if 'id' not in request.session:
        messages.add_message(request, messages.ERROR, "You have to log in first.")
        return redirect('/')
    context = {
        'trips': Trip.objects.filter(Q(creator=request.session['id']) | Q(participants=request.session['id'])).distinct() ,
        'other_trips': Trip.objects.exclude(Q(creator=request.session['id']) | Q(participants=request.session['id'])).distinct()
    }
    return render(request, 'app2/app2_index.html', context)
def add(request):
    if 'id' not in request.session:
        messages.add_message(request, messages.ERROR, "You have to log in first.")
        return redirect('/')
    return render(request, 'app2/add.html')
def add_trip(request):
    errors = Trip.objects.trip_validation(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/travels/add')
    else:
        Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date=request.POST['travel_from'], end_date=request.POST['travel_to'], creator=User.objects.get(id=request.session['id']))
        return redirect('/travels')
def view_trip(request, number):
    if 'id' not in request.session:
        messages.add_message(request, messages.ERROR, "You have to log in first.")
        return redirect('/')
    context = {
        'trip': Trip.objects.get(id=number)
    }
    return render(request, 'app2/view.html', context)
def join_trip(request, number):
    Trip.objects.get(id=number).participants.add(request.session['id'])
    return redirect('/travels')
