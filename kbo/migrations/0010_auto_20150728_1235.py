# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0009_auto_20150728_1226'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set([('date', 'seq', 'home_team', 'away_team')]),
        ),
    ]
