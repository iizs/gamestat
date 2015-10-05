# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0013_expstanding'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='expstanding',
            unique_together=set([('season', 'date', 'team')]),
        ),
    ]
