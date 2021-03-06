from django.contrib import admin

from models import Score, Season, Standing, ExpStanding

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

class ExpStandingAdmin(admin.ModelAdmin):
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

    def season(self, obj):
        return obj.power_ranking.season

    def date(self, obj):
        return obj.power_ranking.date

    def team(self, obj):
        return obj.power_ranking.team
    
admin.site.register(Score, ScoreAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Standing, StandingAdmin)
#admin.site.register(PowerRanking, PowerRankingAdmin)
admin.site.register(ExpStanding, ExpStandingAdmin)
