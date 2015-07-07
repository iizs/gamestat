#-*- coding: utf-8 -*-
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
    # 데이터가 전혀 존재하지 않는 경우에 대해서는 고민하지 않았다.

    latest_standing = Standing.objects.order_by('-date')[0]
    oldest_standing = Standing.objects.order_by('date')[0]
    date = None # 화면에 출력할 기준 날짜

    # 사용자가 valid한 date를 제공했다면, 그 날짜를 사용하되, 
    if basedate != None:
        m = re.match('([0-9]{2,4})([0-9]{2})([0-9]{2})', str(basedate))
        if m != None:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            if year < 100:
                year += 2000
            date = datetime.date(year, month, day)

    # 서버에 데이터가 존재하는 범위 바깥의 날짜라면, 날짜를 그 안쪽으로 조정하고, 
    if date == None or date > latest_standing.date:
        date = latest_standing.date
    elif date < oldest_standing.date:
        date = oldest_standing.date

    # 그 날의 순위 데이터가 없다면, 데이터가 있는 그 전 날짜 중 가장 가까운 날의 데이터를 가져온다.
    standings = Standing.objects.filter(date=date).order_by('-pct', 'wins')
    if len(standings) == 0:
        alternative_standing = Standing.objects.filter(date__lt=date).order_by('-date')[0]
        standings = Standing.objects.filter(date=alternative_standing.date).order_by('-pct', 'wins')

    # prevDate for navigation
    if date == oldest_standing.date:
        prev_date = None
    else:
        prev_standing = Standing.objects.filter(date__lt=date).order_by('-date')[0]
        prev_date = prev_standing.date

    # nextDate for navigation
    if date == latest_standing.date:
        next_date = None
    else:
        next_standing = Standing.objects.filter(date__gt=date).order_by('date')[0]
        next_date = next_standing.date

    template = loader.get_template('kbo/standings.html')
    context = RequestContext(request, {
        'standings' : standings,
        'basedate' : date,
        'startDate' : oldest_standing.date,
        'endDate' : latest_standing.date,
        'prevDate' : prev_date,
        'nextDate' : next_date,
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
