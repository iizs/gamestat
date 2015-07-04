from django.contrib import admin

from models import Score, Season

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
        'draw_option',
    )
    
admin.site.register(Score, ScoreAdmin)
admin.site.register(Season, SeasonAdmin)
