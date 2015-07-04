from django.contrib import admin

from models import Score, Season, Standing

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
    
admin.site.register(Score, ScoreAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Standing, StandingAdmin)
