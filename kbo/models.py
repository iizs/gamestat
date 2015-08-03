#-*- coding: utf-8 -*-
from django.db import models
from django.db import IntegrityError, transaction

import re
import datetime

class Score(models.Model):
    date = models.DateField(db_index=True)
    seq = models.SmallIntegerField()
    home_team = models.CharField(max_length=255, db_index=True)
    away_team = models.CharField(max_length=255, db_index=True)
    home_score = models.SmallIntegerField()
    away_score = models.SmallIntegerField()

    def load_from_daum(self, data):
        year = 0
        month = 0
        day = 0
        lines = data.split('\n')
        for l in lines:
            m = re.search('<td class="time_date"[^>]*>([0-9]+)<span', l)
            if m != None:
                day = int(m.group(1))
                continue

            m = re.search('<td class="cont_score">', l)
            if m != None:
                s = re.sub('<[^>]+>', ' ', l)

                # check if double header
                m = re.search('\(DH([0-9]+)\)', s)
                if m != None:
                    seq = int(m.group(1))
                else:
                    seq = 0

                # parse score
                m = re.search('([^\s]+)\s+([0-9]+)\s*:\s*([0-9]+)\s+([^\s]+)', s)
                if m != None:
                    try:
                        if m.group(1) in [u'이스턴', u'웨스턴', u'동군', u'서군', u'드림', u'나눔' ]:
                            continue

                        date = datetime.date(year, month, day)
                        s_obj = Score( 
                            date=date,
                            home_team=m.group(4),
                            away_team=m.group(1),
                            home_score=int(m.group(3)),
                            away_score=int(m.group(2)),
                            seq = seq,
                        )
                        s_obj.save()
                    except IntegrityError as e:
                        with transaction.atomic():
                            s_org = Score.objects.get(
                                date=date, 
                                home_team=m.group(4),
                                away_team=m.group(1),
                                seq = seq,
                            )

                            if s_org.home_score != s_obj.home_score or s_org.away_score != s_obj.away_score:
                                s_org.delete()
                                s_obj.save()
                    continue

            m = re.search('<em class="txt_day">([0-9]+)</em>.*txt_year', l)
            if m != None:
                year = int(m.group(1))
                continue

            m = re.search('<em class="txt_day">([0-9]+)</em>.*txt_month', l)
            if m != None:
                month = int(m.group(1))
                continue

    class Meta:
        unique_together = (
            ('date', 'seq', 'home_team', 'away_team'),
        )

class Season(models.Model):
    EXHIBITION_GAME = 'eg'
    PENNANT_RACE = 'pr'
    POST_SEASON = 'ps'
    SEASON_TYPE = (
        (EXHIBITION_GAME, 'Exhibition Games'),
        (PENNANT_RACE, 'Pennant Race'),
        (POST_SEASON, 'Post Season'),
    )

    DRAW_NOT_INCLUDED = 'x'
    DRAW_EQ_LOSS = 'l'
    DRAW_EQ_HALF_WIN = 'h'
    DRAW_OPTION = (
        (DRAW_NOT_INCLUDED, 'Exclude draw from PCT'),
        (DRAW_EQ_LOSS, 'Count draw as loss'),
        (DRAW_EQ_HALF_WIN, 'Count draw as 1/2 win'),
    )

    name = models.CharField(max_length=255, unique=True, db_index=True)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    games_per_team = models.SmallIntegerField(null=True, blank=True)
    n_teams = models.SmallIntegerField(null=True, blank=True) # Number of teams
    season_type = models.CharField(max_length=2, choices=SEASON_TYPE, verbose_name = 'Type')
    draw_option = models.CharField(max_length=1, choices=DRAW_OPTION)

    def __unicode__(self):
        return self.name

class Standing(models.Model):
    WIN = 'o'
    LOSS = 'x'
    DRAW = '-'

    season =  models.ForeignKey(Season)
    date = models.DateField(db_index=True)
    team = models.CharField(max_length=255, db_index=True)
    rank = models.SmallIntegerField()
    games = models.SmallIntegerField()
    wins = models.SmallIntegerField()
    losses = models.SmallIntegerField()
    draws = models.SmallIntegerField()
    pct = models.SmallIntegerField()    # PCT * 1000
    gb = models.SmallIntegerField()     # gb * 10
    l10 = models.CharField(max_length=10)   # o is win, x is loss, - is draw
    streak = models.SmallIntegerField() # + is winning streak, - is losing streak
    home_wins = models.SmallIntegerField()
    home_losses = models.SmallIntegerField()
    home_draws = models.SmallIntegerField()

    def save(self, *args, **kwargs):
        try:
            s = Standing.objects.get(
                    season = self.season,
                    date = self.date,
                    team = self.team,
            )
            self.id = s.id
            kwargs['force_update'] = True
        except Standing.DoesNotExist as e:
            kwargs['force_insert'] = True
            self.id = None  # To make new id using AutoField

        super(Standing, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        unique_together = (
            ('season', 'date', 'team'),
        )

    class TeamNotMatched(Exception):
        def __init__(self, message):
            self.message = message
        def __unicode__(self):
            return repr(self.message)

    def apply_score(self, score):
        if len(self.l10) == 10:
            self.l10 = self.l10[1:10]

        if self.team == score.home_team:
            if score.home_score > score.away_score:
                # Home team wins
                self.wins += 1
                self.home_wins += 1
                self.l10 += Standing.WIN
                if self.streak >= 0: 
                    self.streak += 1
                else:
                    self.streak = 1
            elif score.home_score < score.away_score:
                # Home team loses
                self.losses += 1
                self.home_losses += 1
                self.l10 += Standing.LOSS
                if self.streak <= 0: 
                    self.streak -= 1
                else:
                    self.streak = -1
            else:
                # Draw
                self.draws += 1
                self.home_draws += 1
                self.l10 += Standing.DRAW
                self.streak = 0
        elif self.team == score.away_team:
            if score.home_score < score.away_score:
                # Away team wins
                self.wins += 1
                self.l10 += Standing.WIN
                if self.streak >= 0: 
                    self.streak += 1
                else:
                    self.streak = 1
            elif score.home_score > score.away_score:
                # Away team loses
                self.losses += 1
                self.l10 += Standing.LOSS
                if self.streak <= 0: 
                    self.streak -= 1
                else:
                    self.streak = -1
            else:
                # Draw
                self.draws += 1
                self.l10 += Standing.DRAW
                self.streak = 0
        else:
            raise Standing.TeamNotMatched(self.team + ' != ' + score.home_team + ' or ' + score.away_team)

        self.date = score.date
        self.games += 1
        if self.season.draw_option == Season.DRAW_NOT_INCLUDED:
            if self.wins + self.losses > 0:
                self.pct = int(self.wins / float(self.wins + self.losses) * 1000)
            else:
                self.pct = 0
        elif self.season.draw_option == Season.DRAW_EQ_LOSS:
            self.pct = int(self.wins / float(self.games) * 1000)
        elif self.season.draw_option == Season.DRAW_EQ_HALF_WIN:
            self.pct = int((self.wins + 0.5 * self.draws) / float(self.games) * 1000)

    @staticmethod
    def compare_pct(a, b):
        r = b.pct - a.pct
        if r == 0:
            r = b.wins - a.wins
        return r

class PowerRanking(models.Model):
    season =  models.ForeignKey(Season)
    date = models.DateField(db_index=True)
    team = models.CharField(max_length=255, db_index=True)
    power = models.IntegerField()       # * 1,000,000

    def save(self, *args, **kwargs):
        try:
            s = PowerRanking.objects.get(
                    season = self.season,
                    date = self.date,
                    team = self.team,
            )
            self.id = s.id
            kwargs['force_update'] = True
        except PowerRanking.DoesNotExist as e:
            kwargs['force_insert'] = True
            self.id = None  # To make new id using AutoField

        super(PowerRanking, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        unique_together = (
            ('season', 'date', 'team'),
        )

class ExpStanding(models.Model):
    power_ranking = models.ForeignKey(PowerRanking)

    rank = models.SmallIntegerField()
    games = models.SmallIntegerField()
    wins = models.SmallIntegerField()
    losses = models.SmallIntegerField()
    draws = models.SmallIntegerField()
    pct = models.SmallIntegerField()    # PCT * 1000
    gb = models.SmallIntegerField()     # gb * 10

    def save(self, *args, **kwargs):
        try:
            s = ExpStanding.objects.get(
                    power_ranking = self.power_ranking,
            )
            self.id = s.id
            kwargs['force_update'] = True
        except ExpStanding.DoesNotExist as e:
            kwargs['force_insert'] = True
            self.id = None  # To make new id using AutoField

        super(ExpStanding, self).save(*args, **kwargs) # Call the "real" save() method.
