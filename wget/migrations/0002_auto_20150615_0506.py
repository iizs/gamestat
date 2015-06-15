# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wget', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='count_in',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='channel',
            name='count_out',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
