# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-13 06:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20160713_0625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer_id',
            new_name='customer',
        ),
    ]
