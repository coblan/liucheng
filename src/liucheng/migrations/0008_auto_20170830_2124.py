# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-30 13:24
from __future__ import unicode_literals

from django.db import migrations, models
import helpers.base.jsonfield


class Migration(migrations.Migration):

    dependencies = [
        ('liucheng', '0007_auto_20170828_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodegroup',
            name='start_time',
            field=models.DateField(blank=True, null=True, verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='nodegroup',
            name='relations',
            field=helpers.base.jsonfield.JsonField(default=[], verbose_name='\u6d41\u7a0b\u56fe'),
        ),
    ]
