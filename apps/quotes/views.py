# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from ..login_register.models import *
# Create your views here.

def index(request, user_id):
    if 'logged_in' not in request.session:
        messages.error(request, 'Hey Klasshole... You need to Login or Register to access that')
        return redirect('login_register:index')

    template = 'quotes/quotes.html'
    context = {
        'user':User.objects.get(id=user_id),
        'quotes':User.objects.get(id=user_id).quotes.all(),
    }
    return render(request, template, context)
