# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-01 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organize', '0013_auto_20170823_1127'),
        ('liucheng', '0009_auto_20170830_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodegroup',
            name='related_emp',
            field=models.ManyToManyField(blank=True, null=True, to='organize.Employee', verbose_name='\u76f8\u5173\u4eba\u5458'),
        ),
    ]
