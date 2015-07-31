#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

from kbo.models import Score, Season

import datetime

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
    
        # mr stands for match records
        # mr[home][away] = [ wins, losses, draws ]
        mr = {}
        c_date = season.start_date;
        while c_date <= enddate:
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
        
        print 'home.team away.team home.wins away.wins draws'
        for h in mr:
            for a in mr[ h ]:
                line = u'{home} {away} {win} {loss} {draw}'.format( 
                    home = h,
                    away = a,
                    win  = mr[h][a][0],
                    loss = mr[h][a][1],
                    draw = mr[h][a][2],
                )

                print line.encode('utf8')
