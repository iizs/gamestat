# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('channel_id', models.CharField(unique=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('count_in', models.IntegerField()),
                ('count_out', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersistentQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now=True, auto_now_add=True, db_index=True)),
                ('body', models.TextField()),
                ('channel', models.ForeignKey(to='wget.Channel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
