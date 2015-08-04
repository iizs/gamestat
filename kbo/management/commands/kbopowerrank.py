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
import math

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
        self.generate_exp_standings(season, enddate, mr, pr)
        #os.unlink(mr_file)

    def generate_exp_standings(self, season, basedate, mr, pr):
        es = {}
        alt_standing = Standing.objects.filter(date__lt=basedate).order_by('-date')[0]
        standings = Standing.objects.filter(date=alt_standing.date)
        for s in standings:
            es[s.team] = ExpStanding(
                power_ranking = pr[s.team.encode('utf8')],
                rank = 0,
                games = s.games,
                wins = s.wins,
                losses = s.losses,
                draws = s.draws,
                pct = 0,
                gb = 0,
            )

        teams = pr.keys()
        for a in range(0, len(teams)):
            for b in range(a+1, len(teams)):
                team_a = teams[a].decode('utf8')
                team_b = teams[b].decode('utf8')
                pr_a = pr[team_a.encode('utf8')]
                pr_b = pr[team_b.encode('utf8')]
                e = math.exp( ( pr_a.power - pr_b.power ) / float(1000000) )
                prob_a_over_b = e / ( 1 + e )

                a_win = mr[team_a][team_b][0] + mr[team_b][team_a][1]
                b_win = mr[team_a][team_b][1] + mr[team_b][team_a][0]
                draw = mr[team_a][team_b][2] + mr[team_b][team_a][2]

                remain_games = season.games_per_team / ( season.n_teams - 1 ) - a_win - b_win - draw
                exp_win_a = int(round(remain_games * prob_a_over_b))
                exp_win_b = remain_games - exp_win_a
                
                #print '{team_a} ({power_a:0.6f}) v {team_b} ({power_b:0.6f}) : {w}-{l}-{d} with prob({prob:0.5f}) in {remain_games} games {exp_win_a}-{exp_win_b}'.format(
                #    team_a = team_a.encode('utf8'),
                #    team_b = team_b.encode('utf8'),
                #    w = a_win,
                #    l = b_win,
                #    d = draw,
                #    power_a = pr_a.power / float(1000000),
                #    power_b = pr_b.power / float(1000000),
                #    prob = prob_a_over_b,
                #    remain_games = remain_games,
                #    exp_win_a = exp_win_a,
                #    exp_win_b = exp_win_b,
                #)

                es_a = es[team_a]
                es_b = es[team_b]

                es_a.wins += exp_win_a
                es_a.losses += exp_win_b
                es_a.games += remain_games

                es_b.wins += exp_win_b
                es_b.losses += exp_win_a
                es_b.games += remain_games

        Command.calculate_gb(es)
        for k in es:
            es[k].save()
            #print '{team} {g} {w}-{l}-{d} {r} {pct} {gb}'.format(
                #team = es[k].power_ranking.team,
                #g = es[k].games,
                #w = es[k].wins,
                #l = es[k].losses,
                #d = es[k].draws,
                #r = es[k].rank,
                #pct = es[k].pct,
                #gb = es[k].gb,
            #)

    def generate_power_rankings(self, season, basedate, mr_file):
        R_script_file = os.path.join(settings.BASE_DIR, 'BT.Rscript')
        out = subprocess.check_output(["Rscript", R_script_file, mr_file])

        n_teams = 0
        pr = {}
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
                pr[m.group(1)] = o

        if n_teams != season.n_teams:
            raise Command.NotEnoughData('invalid R execution result')

        for k in pr:
            pr[k].save()

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

    @staticmethod
    def calculate_gb(exp_standings):
        l = []
        for k in exp_standings:
            es = exp_standings[k]

            es.pct = Standing.calculate_pct(es, es.power_ranking.season) 
            l.append(es)

        l.sort(cmp=Standing.compare_pct)
        s1 = l[0]
        s1.gb = 0
        rank = 1
        s1.rank = rank

        for s in l[1:]:
            s.gb = int((s1.wins - s.wins + s.losses - s1.losses) / 2.0 * 10)
            rank += 1
            s.rank = rank


