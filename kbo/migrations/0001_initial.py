# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('home_team', models.CharField(max_length=255, db_index=True)),
                ('away_team', models.CharField(max_length=255, db_index=True)),
                ('home_score', models.SmallIntegerField()),
                ('away_score', models.SmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
