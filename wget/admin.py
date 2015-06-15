from django.contrib import admin

from models import Channel, PersistentQueue, PostProcessRule

admin.site.register(Channel)     
admin.site.register(PersistentQueue)     
admin.site.register(PostProcessRule)     
