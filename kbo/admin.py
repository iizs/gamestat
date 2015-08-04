from django.contrib import admin

from models import Score, Season, Standing, PowerRanking

class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'date', 
        'away_team', 
        'away_score', 
        'home_score', 
        'home_team',
    )

class SeasonAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'start_date',
        'end_date',
        'season_type',
        'games_per_team',
        'draw_option',
    )

class StandingAdmin(admin.ModelAdmin):
    list_display = (
        'season',
        'date',
        'team',
        'games',
        'wins',
        'losses',
        'draws',
        'pct',
        'gb',
    )

class PowerRankingAdmin(admin.ModelAdmin):
    list_display = (
        'season',
        'date',
        'team',
        'power_as_float',
    )

    def power_as_float(self, obj):
        return '{f:0.6f}'.format(f = obj.power / float(1000000))
    power_as_float.short_description = 'Power'
    
admin.site.register(Score, ScoreAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Standing, StandingAdmin)
admin.site.register(PowerRanking, PowerRankingAdmin)
