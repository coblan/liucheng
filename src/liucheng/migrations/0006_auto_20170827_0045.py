# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-26 16:45
from __future__ import unicode_literals

from django.db import migrations
import helpers.base.jsonfield


class Migration(migrations.Migration):

    dependencies = [
        ('liucheng', '0005_auto_20170825_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodegroup',
            name='relations',
            field=helpers.base.jsonfield.JsonField(default='[]', verbose_name='\u8282\u70b9\u5173\u7cfb'),
        ),
    ]
