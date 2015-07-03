from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import logging

logger = logging.getLogger(__name__)

def home(request):
    template = loader.get_template('ui/home.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def kbo(request):
    template = loader.get_template('ui/kbo.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def contact(request):
    template = loader.get_template('ui/contact.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
