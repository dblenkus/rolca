# -*- coding: utf-8 -*-
# Generated by Django 1.11a1 on 2017-03-03 23:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_contest_login_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]