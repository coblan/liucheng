# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-08-23 07:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('liucheng', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NodeRecord',
            new_name='NodeGroup',
        ),
        migrations.AddField(
            model_name='worknode',
            name='node_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='liucheng.NodeGroup', verbose_name='\u8282\u70b9\u7ec4'),
        ),
    ]
