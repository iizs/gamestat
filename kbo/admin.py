from django.contrib import admin

from models import Score

class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'date', 
        'away_team', 
        'away_score', 
        'home_score', 
        'home_team',
    )
    
admin.site.register(Score, ScoreAdmin)
