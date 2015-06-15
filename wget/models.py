from django.db import models

class Channel(models.Model):
    channel_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    count_in = models.IntegerField(default=0)
    count_out = models.IntegerField(default=0)

    def __unicode__(self):
        return self.channel_id

class PersistentQueue(models.Model):
    channel = models.ForeignKey('Channel')
    datetime = models.DateTimeField(auto_now=True, auto_now_add=True, db_index=True)
    body = models.TextField()

    def __unicode__(self):
        return str(self.channel) + ' / ' + str(self.datetime)

class PostProcessRule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    pattern = models.CharField(max_length=4096)
    priority = models.SmallIntegerField(db_index=True)
    module_name = models.CharField(max_length=255, null=True, blank=True)
    class_name = models.CharField(max_length=255, null=True, blank=True)
    function_name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def default_processor(self, data):
        pass
    
