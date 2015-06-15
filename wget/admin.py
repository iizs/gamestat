from django.contrib import admin

from models import Channel, PersistentQueue

admin.site.register(Channel)     
admin.site.register(PersistentQueue)     
