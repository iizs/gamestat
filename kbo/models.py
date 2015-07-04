#-*- coding: utf-8 -*-
from django.db import models
from django.db import IntegrityError, transaction

import re
import datetime

class Score(models.Model):
    date = models.DateField(db_index=True)
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
                m = re.search('([^\s]+)\s+([0-9]+)\s*:\s*([0-9]+)\s+([^\s]+)', s)
                if m != None:
                    try:
                        date = datetime.date(year, month, day)
                        s_obj = Score( 
                            date=date,
                            home_team=m.group(4),
                            away_team=m.group(1),
                            home_score=int(m.group(3)),
                            away_score=int(m.group(2)),
                        )
                        s_obj.save()
                    except IntegrityError as e:
                        with transaction.atomic():
                            s_org = Score.objects.get(
                                date=date, 
                                home_team=m.group(4),
                                away_team=m.group(1),
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
            ('date', 'home_team', 'away_team'),
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
    DRAW_EQ_LOST = 'l'
    DRAW_EQ_HALF_WIN = 'h'
    DRAW_OPTION = (
        (DRAW_NOT_INCLUDED, 'Exclude draw from PCT'),
        (DRAW_EQ_LOST, 'Count draw as lost'),
        (DRAW_EQ_HALF_WIN, 'Count draw as 1/2 win'),
    )

    name = models.CharField(max_length=255, unique=True, db_index=True)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    games_per_team = models.SmallIntegerField(null=True, blank=True)
    season_type = models.CharField(max_length=2, choices=SEASON_TYPE, verbose_name = 'Type')
    draw_option = models.CharField(max_length=1, choices=DRAW_OPTION)

    def __unicode__(self):
        return self.name
