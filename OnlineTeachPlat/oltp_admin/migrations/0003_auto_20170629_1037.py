# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oltp_admin', '0002_classinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classinfo',
            name='request_time',
            field=models.TimeField(auto_now=True),
        ),
    ]