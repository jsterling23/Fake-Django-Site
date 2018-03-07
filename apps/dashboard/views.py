# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from ..login_register.models import *

# Create your views here.

# ******** dashboard views *********

def index(request):
    if 'logged_in' not in request.session:
        messages.error(request, 'Hey Klasshole... You need to Login or Register to access that')
        return redirect('login_register:index')

    favs = User.objects.get(id=request.session['user_id']).user_favorite.all().values_list('quote_id', flat = True)

    quotes = Quote.objects.exclude(id__in=favs)

    context = {
        'quotes':quotes,
        'user_favorites':User.objects.get(id=request.session['user_id']).user_favorite.all(),
    }

    template = 'dashboard/dashboard.html'
    return render(request, template, context)










def add_quote(request):
    if 'logged_in' not in request.session:
        messages.error(request, 'Hey Klasshole... You need to Login or Register to access that')
        return redirect('login_register:index')

    if request.method == "POST":
        errors = Quote.objects.quote_validator(request.POST)

        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('dashboard:index')

        content_by = request.POST['content_by']
        message = request.POST['message']
        user = User.objects.get(id=request.session['user_id'])

        Quote.objects.create(content_by=content_by,content=message,user=user)


        print content_by
        print message

        return redirect('dashboard:index')

    return redirect('dashboard:index')










def add_favorite(request, quote_id):
    if 'logged_in' not in request.session:
        messages.error(request, 'Hey Klasshole... You need to Login or Register to access that')
        return redirect('login_register:index')

    if request.method == "POST":

        # quote = quote_id
        user = User.objects.get(id=request.session['user_id'])
        quote = Quote.objects.get(id=quote_id)

        Favorite.objects.create(user=user,quote=quote)

        return redirect('dashboard:index')








def remove_favorite(request, fav_id):

    if 'logged_in' not in request.session:
        messages.error(request, 'Hey Klasshole... You need to Login or Register to access that')
        return redirect('login_register:index')

    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])

        favorite = user.user_favorite.get(id=fav_id).delete()

        return redirect('dashboard:index')

    messages.error(request, 'Woah... Something went wrong')
    return redirect('login_register:index')
