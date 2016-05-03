# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_auto_20160424_0230'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='first_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 2, 23, 5, 14, 100659), auto_now_add=True, db_index=True),
            preserve_default=False,
        ),
    ]
