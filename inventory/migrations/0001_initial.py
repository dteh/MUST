# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-22 13:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=20)),
                ('cost_per_day', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=13)),
                ('is_uom_student', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('gender_id', models.AutoField(primary_key=True, serialize=False)),
                ('gender_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Category')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Gender')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('order_length', models.IntegerField()),
                ('order_due', models.DateField()),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('size_id', models.AutoField(primary_key=True, serialize=False)),
                ('size_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='createdby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.User'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Customer'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_items',
            field=models.ManyToManyField(to='inventory.Item'),
        ),
        migrations.AddField(
            model_name='item',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Size'),
        ),
    ]