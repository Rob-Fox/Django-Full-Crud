# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import users, trips
from django.contrib import messages
import bcrypt, datetime

# Create your views here.

def index(request):
    request.session['user'] = 0
    # user = users.objects.all()
    # print '*'*50
    # print user
    # user.delete()
    # print user
    # print '*'*50
    return render(request, 'login_reg_app/index.html')

def registration(request):
    errors = users.objects.reg_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
           messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        p_word = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = users.objects.create(name=request.POST['name'], user_name=request.POST['user_name'], password=p_word)
        user.save()
        # print '*'*50
        # print user.name
        # print user.user_name
        # print'*'*50
        request.session['user'] = user.id
        # print request.session['user']
        # print '*'*50
        return redirect('/success')
    
def login(request):
    errors = users.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
           messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        # print'*'*50
        # print users.objects.get(user_name=request.POST['l_user_name']).id
        # print'*'*50
        request.session['user'] = users.objects.get(user_name=request.POST['l_user_name']).id
        return redirect('/success')


def success(request):
    today = datetime.datetime.now()
    # print'*'*50
    now =  str(today.year)+ str(today.month)+ str(today.day)
    # print now
    # print'*'*50
    if request.session['user'] == 0:
        return redirect('/')
    user = users.objects.get(id=request.session['user'])
    trip = trips.objects.filter(planner=user.id)
    trip2 = trips.objects.filter(joiners__id=user.id).exclude(planner=user.id).order_by('s_date')
    # print user.name
    context = {
        'name':user.name,
        'users_trips': trips.objects.filter(planner=request.session['user']).order_by('s_date'),
        'more_users_trips': trip2,
        'others_trips': trips.objects.exclude(planner=request.session['user']).exclude(joiners__id=user.id,).order_by('s_date'),

    }
    # print'*'*50
    # print context
    # print trip
    # print'*'*50
    # user = users.objects.filter(id=id)
    return render(request, 'login_reg_app/travels.html',context)

def add_trip(request):
    if request.session['user'] == 0:
        return redirect('/')
    return render(request, 'login_reg_app/add.html')

def process_trip(request):
    # now = datetime.datetime.now()
    today = str(datetime.date.today())
    # now = str(today.year) +'-'+ str(today.month) +'-'+ str(today.day)
    if request.session['user'] == 0:
        return redirect('/')
    user = users.objects.get(id=request.session['user'])
    # print user
    # print '*' *50
    # if request.POST['s_date'] >= request.POST['e_date']:
    #     print '+'*50
    if request.POST['destination'] != '':
        if request.POST['description'] != '':
            if request.POST['s_date'] != '':
                if request.POST['s_date'] >= today:
                    print'*'*50
                    print today
                    # now.strftime('%Y %m %d')
                    # print now
                    print request.POST['s_date']
                    print'*'*50
                    if request.POST['e_date'] != '':
                        if request.POST['s_date'] <= request.POST['e_date']:
                            # print '-'*50
                            trips.objects.create(planner=users.objects.get(id=request.session['user']), description=request.POST['description'], destination=request.POST['destination'], s_date=request.POST['s_date'], e_date=request.POST['e_date'])
                            this_trip = trips.objects.last()
                            this_trip.joiners.add(user)
                            return redirect('/success')
    # res=request.POST['s_date']
    # print '*'*50
    # print res
    # print '*'*50
    print today
    return HttpResponse('failed')

def join(request, number):
    if request.session['user'] == 0:
        return redirect('/')
    user = users.objects.get(id=request.session['user'])
    this_trip = trips.objects.get(id=number)
    this_trip.joiners.add(user)
    return redirect('/success')

def destination(request, number):
    trip = trips.objects.get(id=number)
    context = {
        'destination':trip.destination,
        'planner': trip.planner,
        'description': trip.description,
        's_date': trip.s_date,
        'e_date': trip.e_date,
        'joiners': trip.joiners.all().exclude(id=trip.planner.id),
    }
    # print '*'*50
    # print context['joiners']
    # print '*'*50
    return render(request, 'login_reg_app/destination.html', context)

def dele(request):
    trip = trips.objects.all()
    trip.delete()
    return redirect('/success')
