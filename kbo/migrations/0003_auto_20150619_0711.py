# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0002_auto_20150619_0650'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set([('date', 'home_team', 'away_team')]),
        ),
    ]
