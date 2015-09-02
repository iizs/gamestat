#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Q

import logging
import datetime
import re

from models import Score, Standing, ExpStanding, Season

logger = logging.getLogger(__name__)

def _string2date(s, regex='([0-9]{2,4})/([0-9]{2})/([0-9]{2})'):
    date = None
    if s != None:
        m = re.match(regex, str(s))
        if m != None:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            if year < 100:
                year += 2000
            date = datetime.date(year, month, day)
    return date

def overview(request):
    template = loader.get_template('kbo/overview.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def versus(request):
    latest_score = Score.objects.order_by('-date')[0]
    oldest_score = Score.objects.order_by('date')[0]

    team1 = ''
    team2 = ''
    fromdate = '----/--/--'
    todate = '----/--/--'

    try:
        team1 = request.GET['team1']
        team2 = request.GET['team2']
        fromdate = request.GET['fromdate']
        todate = request.GET['todate']

        fromdate_date = _string2date(str(fromdate))
        if fromdate_date == None:
            fromdate_date = oldest_score.date

        todate_date = _string2date(str(todate))
        if todate_date == None:
            todate_date = latest_score.date

        if team2 != '' :
            scores = Score.objects.filter(
                Q(
                    date__gte = fromdate_date,
                    date__lte = todate_date, 
                    home_team = team1, 
                    away_team = team2, 
                ) | Q (
                    date__gte = fromdate_date,
                    date__lte = todate_date, 
                    home_team = team2, 
                    away_team = team1, 
                )
            ).order_by('date')
        else:
            scores = Score.objects.filter(
                Q(
                    date__gte = fromdate_date,
                    date__lte = todate_date, 
                    home_team = team1, 
                ) | Q (
                    date__gte = fromdate_date,
                    date__lte = todate_date, 
                    away_team = team1, 
                )
            ).order_by('date')
    except KeyError as e:
        scores = None

    template = loader.get_template('kbo/versus.html')
    context = RequestContext(request, {
        'startDate' : oldest_score.date,
        'endDate' : latest_score.date,
        'team1' : team1,
        'team2' : team2,
        'fromdate' : fromdate,
        'todate' : todate,
        'scores' : scores,
    })
    return HttpResponse(template.render(context))

def _get_dates(season, fromdate, todate):
    fromdate_date = _string2date(str(fromdate))
    todate_date = _string2date(str(todate))
    s = Season.objects.get(name=season)

    if fromdate_date == None or fromdate_date < s.start_date:
        fromdate_date = s.start_date
    if todate_date == None or todate_date < s.end_date:
        todate_date = s.end_date

    return (fromdate_date, todate_date)

def _graphs_exp_standings(request, season, fromdate, todate):
    (fromdate_date, todate_date) = _get_dates(season, fromdate, todate)

    teams = ExpStanding.objects.filter(date=todate_date).order_by('rank')
    if len(teams) == 0:
        alternative_standing = ExpStanding.objects.filter(date__lt=todate_date).order_by('-date')[0]
        teams = ExpStanding.objects.filter(date=alternative_standing.date).order_by('rank')

    index = []
    for t in teams:
        index.append(t.team)

    standings = ExpStanding.objects.filter(
        date__gte=fromdate_date,
        date__lte=todate_date,
        season = teams[0].season,
    ).order_by('date', 'rank')

    data = []
    row = []
    date = standings[0].date
    for s in standings:
        if date != s.date:
            data.append(row)
            row=[]
            date = s.date
        row.append(s)
    template = loader.get_template('kbo/graphs_standings_pct.html')
    title = "ExpStandings"
    subtitle = "pct"
    return (index, data, template, title, subtitle)

def _graphs_standings(request, season, fromdate, todate):
    (fromdate_date, todate_date) = _get_dates(season, fromdate, todate)

    teams = Standing.objects.filter(date=todate_date).order_by('rank')
    if len(teams) == 0:
        alternative_standing = Standing.objects.filter(date__lt=todate_date).order_by('-date')[0]
        teams = Standing.objects.filter(date=alternative_standing.date).order_by('rank')

    index = []
    for t in teams:
        index.append(t.team)

    standings = Standing.objects.filter(
        date__gte=fromdate_date,
        date__lte=todate_date,
        season = teams[0].season,
    ).order_by('date', 'rank')

    data = []
    row = []
    date = standings[0].date
    for s in standings:
        if date != s.date:
            data.append(row)
            row=[]
            date = s.date
        row.append(s)
    template = loader.get_template('kbo/graphs_standings_pct.html')
    title = "Standings"
    subtitle = "pct"
    return (index, data, template, title, subtitle)


def graphs(request):
    latest_score = Score.objects.order_by('-date')[0]
    oldest_score = Score.objects.order_by('date')[0]
    seasons = Season.objects.all()
    template = loader.get_template('kbo/graphs_base.html')

    try:
        fromdate = request.GET['fromdate']
        todate = request.GET['todate']
        g_type = request.GET['graph_type']
        season = request.GET['season']
    except KeyError as e:
        fromdate = '----/--/--'
        todate = '----/--/--'
        g_type = ''
        season = ''

    if g_type in ['standings_pct']:
        (index, data, template, title, subtitle) = _graphs_standings(request, season, fromdate, todate)
    elif g_type in ['exp_standings_pct']:
        (index, data, template, title, subtitle) = _graphs_exp_standings(request, season, fromdate, todate)
    else :
        index = []
        data = []
        template = loader.get_template('kbo/graphs_standings_pct.html')
        title = ''
        subtitle = ''

    context = RequestContext(request, {
        'graph_type' : g_type,
        'seasons' : seasons,
        'season' : season,
        'data' : data,
        'index' : index,
        'title' : title,
        'subtitle' : subtitle,
        'fromdate' : fromdate,
        'todate' : todate,
        'startDate' : oldest_score.date,
        'endDate' : latest_score.date,
    })
    return HttpResponse(template.render(context))

def standings(request, basedate=None):
    # 데이터가 전혀 존재하지 않는 경우에 대해서는 고민하지 않았다.

    latest_standing = Standing.objects.order_by('-date')[0]
    oldest_standing = Standing.objects.order_by('date')[0]
    date = None # 화면에 출력할 기준 날짜

    # 사용자가 valid한 date를 제공했다면, 그 날짜를 사용하되, 
    date = _string2date(str(basedate), regex='([0-9]{2,4})([0-9]{2})([0-9]{2})')

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
        prev_date = date - datetime.timedelta(days=1)

    # nextDate for navigation
    if date == latest_standing.date:
        next_date = None
    else:
        next_date = date + datetime.timedelta(days=1)

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

    date = _string2date(str(basedate), regex='([0-9]{2,4})([0-9]{2})([0-9]{2})')

    if date == None:
        date = latest_score.date

    scores = Score.objects.filter(date=date)

    # prevDate for navigation
    if date == oldest_score.date:
        prev_date = None
    else:
        prev_date = date - datetime.timedelta(days=1)

    # nextDate for navigation
    if date == latest_score.date:
        next_date = None
    else:
        next_date = date + datetime.timedelta(days=2)

    template = loader.get_template('kbo/scores.html')
    context = RequestContext(request, {
        'scores' : scores,
        'basedate' : date,
        'startDate' : oldest_score.date,
        'endDate' : latest_score.date,
        'prevDate' : prev_date,
        'nextDate' : next_date,
    })
    return HttpResponse(template.render(context))
