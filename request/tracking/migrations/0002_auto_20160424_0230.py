# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='first_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 24, 2, 30, 23, 726587), auto_now_add=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visit',
            name='last_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 24, 2, 30, 30, 38823), auto_now=True, db_index=True),
            preserve_default=False,
        ),
    ]
