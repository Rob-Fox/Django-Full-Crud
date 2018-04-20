# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')

# Create your models here.

class users_manager(models.Manager):
    def reg_validator(self, postData):
        errors={}
        if len(postData['name']) < 3:
            errors["name"] = "Name has to be more than 2 characters long"
        if not NAME_REGEX.match(postData['name']):
            errors['name'] = 'Name must be comprised of letters only'
        if len(postData['user_name']) < 3:
            errors["user_name"] = "Username has to be more than 2 characters long"
        if not NAME_REGEX.match(postData['user_name']):
            errors['user_name'] = 'Username must be comprised of letters only'
        # if not EMAIL_REGEX.match(postData['email']):
        #     errors['email'] = 'Please enter a valid email'
        if users.objects.filter(user_name = postData['user_name']):
            errors['user_name'] = 'You have already registered or that Username is already taken'
        if len(postData['password']) < 8:
            errors['password'] = 'Please enter a password that is 8 characters or longer'
        if postData['password'] != postData['c_password']:
            errors['password'] = 'Please confirm your password'
        return errors

    def login_validator(self, postData):
        errors={}
        # email = postData['l_email']
        # if not EMAIL_REGEX.match(postData['l_email']):
        #     errors['l_email'] = 'Please enter a valid email'
        if not users.objects.filter(user_name = postData['l_user_name']):
            errors['l_user_name'] = "Looks like that User doesn't have an account"
        if len(postData['l_password']) < 8:
            errors['l_password'] = 'Please enter a valid password'
        if users.objects.filter(user_name = postData['l_user_name']):
            if not bcrypt.checkpw(postData['l_password'].encode(), users.objects.get(user_name = postData['l_user_name']).password.encode()):
                errors['l_password'] = 'Wrong password, try again'
        return errors

class users(models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    # email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    objects = users_manager()

    def __repr__(self):
        return 'Name: {}, Username: {}, Password: {}'.format(self.name, self.user_name, self.password)


class trips(models.Model):
    planner = models.ForeignKey(users, related_name='planned')
    description = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    s_date = models.DateField(auto_now=False, auto_now_add=False)
    e_date = models.DateField(auto_now=False, auto_now_add=False)
    joiners = models.ManyToManyField(users, related_name='joining')
