# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0004_alter_time_timezone_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('last_time', models.DateTimeField(auto_now=True, db_index=True)),
                ('requests', models.ManyToManyField(to='request.Request')),
            ],
            options={
                'verbose_name': 'visit',
                'verbose_name_plural': 'visits',
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('first_time', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'verbose_name': 'visitor',
                'verbose_name_plural': 'visitors',
            },
        ),
        migrations.AddField(
            model_name='visit',
            name='visitor',
            field=models.ForeignKey(to='tracking.Visitor'),
        ),
    ]
