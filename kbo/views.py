from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import logging
import datetime
import re

from models import Score

logger = logging.getLogger(__name__)

def overview(request):
    template = loader.get_template('kbo/overview.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def standings(request):
    template = loader.get_template('kbo/standings.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def scores(request, basedate=None):
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
        score = Score.objects.order_by('-date')[0]
        date = score.date

    scores = Score.objects.filter(date=date)
    template = loader.get_template('kbo/scores.html')
    context = RequestContext(request, {
        'scores' : scores,
        'basedate' : date,
    })
    return HttpResponse(template.render(context))
