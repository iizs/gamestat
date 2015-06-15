# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wget', '0002_auto_20150615_0506'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostProcessRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('pattern', models.CharField(max_length=4096)),
                ('priority', models.SmallIntegerField(db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
