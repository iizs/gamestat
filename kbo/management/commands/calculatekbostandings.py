from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

from kbo.models import Score, Season, Standing

import datetime

class Command(BaseCommand):
    help = 'Calculate KBO standings'
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
        make_option('--force',
            action='store_true',
            dest='force',
            default=False,
            help='force to re-calculate standings even if already calculated',
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

        force = options['force']

        standings = {}
        # TODO populate p_standings
        c_date = startdate;
        while c_date <= enddate:
            print c_date

            scores = Score.objects.filter(date=c_date)
            if len(scores) > 0:
                for s in scores:
                    standings.update(Command.apply_score(standings, season, s))

                Command.calculate_gb(standings)
                
                for k in standings:
                    s = standings[k]
                    s.date = c_date # if not, date field not updated for teams that had no game on this day
                    s.save()

            c_date = c_date + datetime.timedelta(days=1)
            #p_standings = c_standings

    @staticmethod
    def get_standing(standings, season, team, date):
        if team in standings:
            standing = standings[team]
        else:
            standing = Standing(
                season = season,
                date = date, 
                team = team,
                l10 = '',
                games = 0, 
                wins = 0,
                losses = 0, 
                draws = 0, 
                pct = 0, 
                gb = 0, 
                streak = 0, 
                home_wins = 0,
                home_losses = 0, 
                home_draws = 0, 
            )

        return standing

    @staticmethod
    def apply_score(standings, season, score):
        home_standing = Command.get_standing(standings, season, score.home_team, score.date)
        away_standing = Command.get_standing(standings, season, score.away_team, score.date)

        home_standing.apply_score(score)
        away_standing.apply_score(score)
        return {
            score.home_team : home_standing,
            score.away_team : away_standing,
        }

    @staticmethod
    def calculate_gb(standings):
        l = []
        for s in standings:
            l.append(standings[s])

        l.sort(cmp=Standing.compare_pct)
        s1 = l[0]
        s1.gb = 0

        for s in l[1:]:
            s.gb = int((s1.wins - s.wins + s.losses - s1.losses) / 2.0 * 10)
