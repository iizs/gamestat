from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

from kbo.models import Score, Season

import datetime

class Command(BaseCommand):
    help = 'Remove KBO scores'
    option_list = BaseCommand.option_list + (
        make_option('--season',
            action='store',
            type='string',
            dest='season',
            default=None,
            help='SEASON name to calculate standings',
        ),
        make_option('--end-date',
            action='store',
            type='string',
            dest='enddate',
            default=None,
            help='last date to calculate standings (YYYYmmdd)',
        ),
        make_option('--start-date',
            action='store',
            type='string',
            dest='startdate',
            default=None,
            help='first date to calculate standings (YYYYmmdd)',
        ),
    )

    def handle(self, *args, **options):
        if options['season'] == None:
            raise CommandError('missing arguments; SEASON must be provided')

        try:
            season = Season.objects.get(name=options['season'])
        except Season.DoesNotExist as e:
            raise CommandError('SEASON not found')

        if options['startdate'] != None:
            startdate = datetime.datetime.strptime(options['startdate'], '%Y%m%d').date()
            if startdate < season.start_date:
                startdate = season.start_date
        else:
            startdate = season.start_date

        if options['enddate'] != None:
            enddate = datetime.datetime.strptime(options['enddate'], '%Y%m%d').date()
            if enddate > season.end_date:
                enddate = season.end_date
        else:
            enddate = season.end_date
    
        c_date = startdate;
        while c_date <= enddate:
            scores = Score.objects.filter(date=c_date)
            if len(scores) > 0:
                print c_date
                for s in scores:
                    s.delete()

            c_date = c_date + datetime.timedelta(days=1)
