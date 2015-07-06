# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0006_auto_20150704_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standing',
            name='l10',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
