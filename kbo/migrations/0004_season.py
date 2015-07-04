# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0003_auto_20150619_0711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, db_index=True)),
                ('start_date', models.DateField(db_index=True)),
                ('end_date', models.DateField(db_index=True)),
                ('season_type', models.CharField(max_length=2, verbose_name=b'Type', choices=[(b'eg', b'Exhibition Games'), (b'pr', b'Pennant Race'), (b'ps', b'Post Season')])),
                ('draw_option', models.CharField(max_length=1, choices=[(b'x', b'Exclude draw from PCT'), (b'l', b'Count draw as lost'), (b'h', b'Count draw as 1/2 win')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
