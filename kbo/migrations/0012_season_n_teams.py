# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0011_auto_20150803_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='n_teams',
            field=models.SmallIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
