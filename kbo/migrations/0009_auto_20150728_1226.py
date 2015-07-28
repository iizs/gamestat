# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0008_standing_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='seq',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
