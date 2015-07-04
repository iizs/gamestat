# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbo', '0005_season_games_per_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Standing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(db_index=True)),
                ('team', models.CharField(max_length=255, db_index=True)),
                ('games', models.SmallIntegerField()),
                ('wins', models.SmallIntegerField()),
                ('losses', models.SmallIntegerField()),
                ('draws', models.SmallIntegerField()),
                ('pct', models.SmallIntegerField()),
                ('gb', models.SmallIntegerField()),
                ('l10', models.SmallIntegerField()),
                ('streak', models.SmallIntegerField()),
                ('home_wins', models.SmallIntegerField()),
                ('home_losses', models.SmallIntegerField()),
                ('home_draws', models.SmallIntegerField()),
                ('season', models.ForeignKey(to='kbo.Season')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='standing',
            unique_together=set([('season', 'date', 'team')]),
        ),
        migrations.AlterField(
            model_name='season',
            name='draw_option',
            field=models.CharField(max_length=1, choices=[(b'x', b'Exclude draw from PCT'), (b'l', b'Count draw as loss'), (b'h', b'Count draw as 1/2 win')]),
            preserve_default=True,
        ),
    ]
