# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
import bcrypt
import datetime

# Create your views here.

# ****** login views *********

def index(request):

    template ='login_register/login_register.html'
    return render(request, template)





# ***Process the registration data****

def register(request):
    if request.method == "POST":

        name = request.POST['name']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        dob = request.POST['dob']

        form_errors = User.objects.register_validator(request.POST)

        if len(form_errors):
            for tag, error in form_errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('login_register:index'))


        db_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

# ***Not 100% sure if I should create users in the views when it could be done in the manager...
# ***But then again isn't the manager for validations only?***

        User.objects.create(
            name=name,
            alias=alias,
            email=email,
            password=db_password,
            dob=dob,
        )
        messages.success(request, "Thank you for registering!")
        messages.success(request, "Please login to access the site")
        return redirect(reverse('login_register:index'))

    else:
        messages.error(request, "No No No! You cannot bypass my python!... If you can email me bro...")
        return redirect(reverse('login_register:index'))

    return redirect(reverse('login_register:index'))









def login(request):
    if request.method == "POST":
        errors = User.objectsTwo.login_validator(request.POST)

        if errors != None:
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect(reverse('login_register:index'))

        user = User.objects.get(email=request.POST['email'])
        user_id = user.id
        user_name = user.name

        request.session['user_id'] = user_id
        request.session['user_name'] = user_name
        request.session['logged_in'] = 'logged_in'

        return redirect(reverse('dashboard:index'))

    return redirect(reverse('login_register:index'))







def logout(request):
    del request.session['logged_in']
    del request.session['user_name']
    del request.session['user_id']
    return redirect('login_register:index')








# Just gives data so I can see the database.

def peek(request):
    context = {
        'users':User.objects.all().values(),

    }
    template = 'login_register/peek.html'
    return render(request, template, context)
