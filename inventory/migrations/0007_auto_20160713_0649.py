# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-13 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20160713_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
