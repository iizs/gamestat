# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0007_auto_20150705_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='standing',
            name='rank',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
