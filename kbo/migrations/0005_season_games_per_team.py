# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0004_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='games_per_team',
            field=models.SmallIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
