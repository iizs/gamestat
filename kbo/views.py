from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

import logging

logger = logging.getLogger(__name__)

def home(request):
    template = loader.get_template('kbo/home.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
