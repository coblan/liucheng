# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-03 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liucheng', '0011_auto_20170903_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodegroup',
            name='start_time',
        ),
        migrations.AddField(
            model_name='worknode',
            name='start_time',
            field=models.CharField(blank=True, max_length=100, verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
    ]
