# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0012_season_n_teams'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpStanding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(db_index=True)),
                ('team', models.CharField(max_length=255, db_index=True)),
                ('power', models.IntegerField()),
                ('rank', models.SmallIntegerField()),
                ('games', models.SmallIntegerField()),
                ('wins', models.SmallIntegerField()),
                ('losses', models.SmallIntegerField()),
                ('draws', models.SmallIntegerField()),
                ('pct', models.SmallIntegerField()),
                ('gb', models.SmallIntegerField()),
                ('season', models.ForeignKey(to='kbo.Season')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
