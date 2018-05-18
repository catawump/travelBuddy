from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import re
import bcrypt

class userManager(models.Manager):
    def register(self,request):

        if len(request.POST["name"]) < 1:
			messages.add_message( request, messages.ERROR, "Name is required!" )
        if len(request.POST["username"]) < 1:
			messages.add_message( request, messages.ERROR, "Username is required!" )
        if len(request.POST["password"]) < 8:
			messages.add_message( request, messages.ERROR, "Password must be between 8-32 characters!" )
        if request.POST["password"] != request.POST["confirm_password"]:
			messages.add_message( request, messages.ERROR, "Password and Password Confirmation must match!" )
        if User.objects.filter(username=request.POST["username"]).count() > 0:
			messages.add_message( request, messages.ERROR, "A user with this username already exists!" )
#If there are error messages at the end, return false.
        if len(get_messages(request)) > 0:
            return False
#Else, create the user and hash the password.
        else:

            User.objects.create(
                name = request.POST["name"],
                username = request.POST["username"],
                password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            )
            messages.add_message (request, messages.ERROR, "Your account has been created!")
            return True

#User Model

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = userManager()

#Destination Model

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    trip_creator = models.ForeignKey(User, related_name="user_trips")
    trip_travelers = models.ManyToManyField(User, related_name="trip_travelers")
    travel_start = models.DateField()
    travel_end = models.DateField()