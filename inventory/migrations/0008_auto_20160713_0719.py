# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-13 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20160713_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cpd',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
