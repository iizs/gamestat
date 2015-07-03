from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import logging

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

def scores(request):
    template = loader.get_template('kbo/scores.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
