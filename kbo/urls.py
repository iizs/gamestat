from django.conf.urls import patterns, include, url
from django.contrib import admin

import views

urlpatterns = patterns('',
    url(r'^$', views.overview, name='overview'),
    url(r'scores/$', views.scores, name='scores'),
    url(r'scores/(?P<basedate>\d+)/$', views.scores, name='scores_on'),
    url(r'standings/$', views.standings, name='standings'),
    url(r'standings/(?P<basedate>\d+)/$', views.standings, name='standings_on'),
)
