from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^reg$', views.registration),
    url(r'^success$', views.success),
    url(r'login$', views.login),
    url(r'^success/add$', views.add_trip),
    url(r'^success/add/proc$', views.process_trip),
    url(r'^success/join/(?P<number>\d+)$', views.join),
    url(r'^success/destination/(?P<number>\d+)$', views.destination),
    url(r'^delete$', views.dele),
]
