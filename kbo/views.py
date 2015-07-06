from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import logging
import datetime
import re

from models import Score, Standing

logger = logging.getLogger(__name__)

def overview(request):
    template = loader.get_template('kbo/overview.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def standings(request, basedate=None):
    latest_standing = Standing.objects.order_by('-date')[0]
    oldest_standing = Standing.objects.order_by('date')[0]
    date = None

    if basedate != None:
        m = re.match('([0-9]{2,4})([0-9]{2})([0-9]{2})', str(basedate))
        if m != None:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            if year < 100:
                year += 2000
            date = datetime.date(year, month, day)

    if date == None:
        date = latest_standing.date

    standings = Standing.objects.filter(date=date).order_by('-pct', 'wins')

    template = loader.get_template('kbo/standings.html')
    context = RequestContext(request, {
        'standings' : standings,
        'basedate' : date,
        'startDate' : oldest_standing.date,
        'endDate' : latest_standing.date,
    })
    return HttpResponse(template.render(context))

def scores(request, basedate=None):
    latest_score = Score.objects.order_by('-date')[0]
    oldest_score = Score.objects.order_by('date')[0]
    date = None

    if basedate != None:
        m = re.match('([0-9]{2,4})([0-9]{2})([0-9]{2})', str(basedate))
        if m != None:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            if year < 100:
                year += 2000
            date = datetime.date(year, month, day)

    if date == None:
        date = latest_score.date

    scores = Score.objects.filter(date=date)
    template = loader.get_template('kbo/scores.html')
    context = RequestContext(request, {
        'scores' : scores,
        'basedate' : date,
        'startDate' : oldest_score.date,
        'endDate' : latest_score.date,
    })
    return HttpResponse(template.render(context))
