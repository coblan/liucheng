# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-20 16:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workboard', '0002_auto_20170917_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worknode',
            name='work_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workboard.WorkGroup', verbose_name='\u5de5\u4f5c\u8ba1\u5212'),
        ),
    ]
