from django.conf.urls import patterns, include, url
from django.contrib import admin

import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
)
