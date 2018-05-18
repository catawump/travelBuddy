from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import User, Trip
import re
from django.contrib import messages
import bcrypt
from django.db.models import Q
from datetime import date

def index(request):
    if 'name' not in request.session:
        return render (request, "travel/index.html")
    else:
        return render (request, "travel/dashboard.html")

def register(request):
	if request.method == "POST":
		User.objects.register(request)
		return redirect("/")
	else:
		return redirect("/")

def login(request):
    try:
        user = User.objects.get ( username=request.POST["username"] )

        isValid = bcrypt.checkpw( request.POST["password"].encode() , user.password.encode() )
        
        if isValid:
            print ("Password match!")
            request.session['name'] = user.name
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            return redirect ("/dashboard")

        else:
            print ("Passwords do NOT match!")
            messages.add_message (request, messages.ERROR, "Invalid Credentials!")
            return redirect("/")
        
    except:
        messages.add_message (request, messages.ERROR, "No user with this username found!")
        return redirect("/")

def dashboard(request):
    if 'name' not in request.session:
        return render (request, "travel/index.html")
    else:
        currentuserid = request.session['user_id']
        mytrips = Trip.objects.filter(Q(trip_creator_id = currentuserid) | Q(trip_travelers = currentuserid))
        othertrips = Trip.objects.exclude(Q(trip_creator_id = currentuserid) | Q(trip_travelers = currentuserid))
        return render (request, "travel/dashboard.html", {
            "mytrips": mytrips,
            "othertrips": othertrips,
        })

def add(request):
    if 'name' not in request.session:
        return render (request, "travel/index.html")
    else:
        return render (request, "travel/addtrip.html")

def createtrip(request):
    today = str(date.today())

    if 'name' not in request.session:
        return render (request, "travel/index.html")
    else:
        if request.method == "POST":
            if len(request.POST["destination"]) < 1:
                messages.add_message( request, messages.ERROR, "Destination cannot be blank!" )
                return redirect("/add")
            if len(request.POST["plan"]) < 1:
                messages.add_message( request, messages.ERROR, "Plan cannot be blank!" )
                return redirect("/add")
            if len(request.POST["startdate"]) < 1:
                messages.add_message( request, messages.ERROR, "Trip Start Date cannot be blank!" )
                return redirect("/add")
            if len(request.POST["enddate"]) < 1:
                messages.add_message( request, messages.ERROR, "Trip End Date cannot be blank!" )
                return redirect("/add")
            if request.POST["startdate"] > request.POST["enddate"]:
                messages.add_message( request, messages.ERROR, "Trip Start Date cannot be after End Date!" )
                return redirect("/add")
            if request.POST["startdate"] < today or request.POST["enddate"] < today:
                messages.add_message( request, messages.ERROR, "Dates must be in the future!" )
                return redirect("/add")
            else:
                trip = Trip.objects.create(
                    destination = request.POST["destination"],
                    plan = request.POST["plan"],
                    travel_start = request.POST["startdate"],
                    travel_end = request.POST["enddate"],
                    trip_creator_id = request.session['user_id'],
                )

                messages.add_message( request, messages.ERROR, "Your trip has been added!" )
                return redirect("/dashboard")
        else:
            return redirect("/add")

def showtrip(request, id):
    if 'name' not in request.session:
        return render (request, "travel/index.html")
    else:
        trip = Trip.objects.get(id=id) 
        context= {
            "trip": trip,
            'travelers': User.objects.filter(trip_travelers__id=id),
        }
        return render (request, "travel/showtrip.html", context)

def jointrip(request, id):
    if 'name' not in request.session:
        return render (request, "travel/index.html")
    else:
        user = User.objects.get(id = request.session['user_id'])
        trip = Trip.objects.get(id=id)
        trip.trip_travelers.add(user)
        trip.save()
        messages.add_message( request, messages.ERROR, "You joined a trip!" )
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect("/")