from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import logging
import datetime

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
    date = datetime.date(2015, 05, 05)
    scores = Score.objects.filter(date=date)
    template = loader.get_template('kbo/scores.html')
    context = RequestContext(request, {
        'scores' : scores,
    })
    return HttpResponse(template.render(context))
