#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings

from optparse import make_option

from kbo.models import Score, Season, Standing, PowerRanking, ExpStanding

import datetime
import subprocess
import string
import os
import re

class Command(BaseCommand):
    help = 'Print KBO match records between teams'
    option_list = BaseCommand.option_list + (
        make_option('--season',
            action='store',
            type='string',
            dest='season',
            default=None,
            help='SEASON name to print match records',
        ),
        make_option('--end-date',
            action='store',
            type='string',
            dest='enddate',
            default=None,
            help='last date to calculate match records (YYYYmmdd)',
        ),
    )

    class NotEnoughData(Exception):
        def __init__(self, message):
            self.message = message
        def __unicode__(self):
            return repr(self.message)

    def handle(self, *args, **options):
        if options['season'] == None:
            raise CommandError('missing arguments; SEASON must be provided')

        try:
            season = Season.objects.get(name=options['season'])
        except Season.DoesNotExist as e:
            raise CommandError('SEASON not found')

        if options['enddate'] != None:
            enddate = datetime.datetime.strptime(options['enddate'], '%Y%m%d').date()
            if enddate > season.end_date:
                enddate = season.end_date
        else:
            enddate = season.end_date

        mr_file = os.path.join(settings.BASE_DIR, 'match_record')
        mr = self.generate_match_record(season, enddate, mr_file)
        pr = self.generate_power_rankings(season, enddate, mr_file)
        #os.unlink(mr_file)

    def generate_power_rankings(self, season, basedate, mr_file):
        R_script_file = os.path.join(settings.BASE_DIR, 'BT.Rscript')
        out = subprocess.check_output(["Rscript", R_script_file, mr_file])

        n_teams = 0
        pr = []
        r = re.compile('^([^\s]+)\s+([\d.-]+)\s+', re.UNICODE)
        for l in string.split(out, '\n'):
            m = r.match(l)
            if m != None:
                n_teams += 1
                o = PowerRanking(
                    season = season,
                    date = basedate,
                    team = m.group(1),
                    power = int(float(m.group(2)) * 1000000),
                )
                pr.append(o)

        if n_teams != season.n_teams:
            raise Command.NotEnoughData('invalid R execution result')

        for o in pr:
            o.save()

        return pr
    
    def generate_match_record(self, season, basedate, outfile_name):
        # mr stands for match records
        # mr[home][away] = [ wins, losses, draws ]

        mr = {}
        c_date = season.start_date;
        while c_date <= basedate:
            scores = Score.objects.filter(date=c_date)
            if len(scores) > 0:
                for s in scores:
                    if s.home_team not in mr:
                        mr[ s.home_team ] = {}

                    if s.away_team not in mr[ s.home_team ]:
                        mr[ s.home_team ][ s.away_team ] = [ 0, 0, 0 ]

                    if s.home_score > s.away_score :
                        mr[ s.home_team ][ s.away_team ][0] += 1
                    elif s.home_score < s.away_score :
                        mr[ s.home_team ][ s.away_team ][1] += 1
                    else:
                        mr[ s.home_team ][ s.away_team ][2] += 1

            c_date = c_date + datetime.timedelta(days=1)

        teams = []
        alt_standing = Standing.objects.filter(date__lt=basedate).order_by('-date')[0]
        standings = Standing.objects.filter(date=alt_standing.date)
        for s in standings:
            teams.append(s.team)

        with open(outfile_name, 'w') as f:
            outfile = File(f)
            outfile.write('home.team away.team home.wins away.wins draws\n')
            for h in teams:
                for a in teams:
                    if h == a:
                        continue
                    if h not in mr:
                        mr[h] = {}

                    if a not in mr[h]:
                        mr[h][a] = [0, 0, 0]

                    line = u'{home} {away} {win} {loss} {draw}\n'.format( 
                        home = h,
                        away = a,
                        win  = mr[h][a][0],
                        loss = mr[h][a][1],
                        draw = mr[h][a][2],
                    )
                    outfile.write(line.encode('utf8'))

        return mr



