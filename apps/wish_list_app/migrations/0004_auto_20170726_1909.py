# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-26 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish_list_app', '0003_auto_20170726_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item',
            field=models.CharField(max_length=255),
        ),
    ]
