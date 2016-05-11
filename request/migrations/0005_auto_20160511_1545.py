# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0004_alter_time_timezone_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='user_agent',
            field=models.CharField(default=b'', max_length=255, null=True, verbose_name='user agent', blank=True),
        ),
    ]
