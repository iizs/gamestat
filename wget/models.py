from django.db import models

class Channel(models.Model):
    channel_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    count_in = models.IntegerField(default=0)
    count_out = models.IntegerField(default=0)

class PersistentQueue(models.Model):
    channel = models.ForeignKey('Channel')
    datetime = models.DateTimeField(auto_now=True, auto_now_add=True, db_index=True)
    body = models.TextField()

