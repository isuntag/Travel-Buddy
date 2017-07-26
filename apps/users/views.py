from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
from datetime import datetime
import bcrypt

def index(request):
    return render(request, 'users/users_index.html')
def register(request):
    # if there are errors in registration form add errors to messages and redirect back to index where form is
    errors = User.objects.validation(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    # if there are no errors encrypt password and save registration form information in db and redirect to travel overview page
    else:
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(name=request.POST['name'], username=request.POST['username'], password=pwhash)
        request.session['name'] = request.POST['name']
        request.session['username'] = request.POST['username']
        request.session['id'] = User.objects.get(username=request.POST['username']).id
        return redirect('/travels')
def signin(request):
    #if there are errors in login form add errors to messages and redirect back to index where form is
    errors = User.objects.login_validation(request.POST)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    #if there are no errors in login form set session username, name, and id for individual user based on entered username and redirect to travel overview page
    else:
        request.session['username'] = request.POST['username']
        request.session['name'] = User.objects.get(username=request.POST['username']).name
        request.session['id'] = User.objects.get(username=request.POST['username']).id
        return redirect('/travels')

def logout(request):
    #when user logs out clear session
    messages.add_message(request, messages.SUCCESS, "You have been logged out.")
    request.session.clear()
    return redirect('/')
