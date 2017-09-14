# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-09-13 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liucheng', '0012_auto_20170903_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worknode',
            name='start_time',
            field=models.CharField(blank=True, max_length=20, verbose_name='\u542f\u52a8\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='worknode',
            name='status',
            field=models.CharField(choices=[('waiting', '\u7b49\u5f85'), ('finish', '\u5b8c\u6210')], default='waiting', max_length=30, verbose_name='\u72b6\u6001'),
        ),
    ]