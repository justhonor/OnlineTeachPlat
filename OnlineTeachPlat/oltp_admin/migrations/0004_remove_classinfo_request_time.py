# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 10:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oltp_admin', '0003_auto_20170629_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classinfo',
            name='request_time',
        ),
    ]