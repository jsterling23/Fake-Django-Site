# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import bcrypt


# Create your models here.

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        now = datetime.datetime.now()
        year = now.year
        birth_year = postData['dob'][:4]

        if len(postData['name']) < 2:
            errors['name'] = "Must enter name"
        if len(postData['alias']) < 2:
            errors['alias'] = "Must enter an Alias"
        if len(postData['email']) < 2:
            errors['email'] = "Must enter an email"
        elif int(year) - int(birth_year) < 18:
            errors['age_restriction'] = "You are too young my child..."
        if len(postData['dob']) < 2:
            errors['dob'] = "Must enter a DOB"
        if len(postData['password']) < 2:
            errors['password'] = "Must enter password"
        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = "Passwords do not match"
        if User.objects.filter(email=postData['email']).exists():
            errors['email_exists'] = "That email already exists! Please try again..."
        return errors



class UserManager_login(models.Manager):
    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) < 2:
            errors['email'] = "Must enter an email"
        if len(postData['password']) < 2:
            errors['password'] = "Must enter password"
        if len(errors):
            return errors

        if User.objects.filter(email=postData['email']).exists():
            user = User.objects.get(email=postData['email'])
        else:
            errors['email_not_exists'] = "That email doesn't exist"
            return errors

        db_password = user.password
        login_password = postData['password']
# **** I put the Try Excpet here because a few of the users I created have plain text passwords and it trips a Salt error here ****
        try:
            bcrypt.checkpw(login_password.encode(), db_password.encode())
        except ValueError as e:
            errors['something_went_wrong'] = "Something went wrong..."
            return errors

        if bcrypt.checkpw(login_password.encode(), db_password.encode()) == False:
            errors['password_incorrect'] = "Password is incorrect"
            return errors
        else:
            return

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['content_by']) < 2:
            errors['content_by'] = "Yo.. I don't know anyone without a name... Try again there buddy."
        if len(postData['message']) < 10:
            errors['message'] = "That was not a quote..."
        return errors




class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    objectsTwo = UserManager_login()

    def __str__(self):
        return ('Name: {}.. Alias: {}.. Email: {}..').format(self.name, self.alias, self.email)

class Quote(models.Model):
    content_by = models.CharField(max_length=255)
    content = models.TextField(max_length=300)
    user = models.ForeignKey(User, related_name='quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __str__(self):
        return ('By: {}.. Quote: {}..').format(self.content_by, self.content)

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='user_favorite')
    quote = models.ForeignKey(Quote, related_name='quotes_info')
    # def __str__(self):
    #     return "User {}... Quote: {}".format(self.user, self.quote)
