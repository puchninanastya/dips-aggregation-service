# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-24 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(max_length=40)),
                ('app_secret', models.CharField(max_length=128)),
                ('token', models.CharField(max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'AppToken',
                'verbose_name_plural': 'AppTokens',
            },
        ),
    ]
