# Generated by Django 3.0rc1 on 2021-02-08 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_extend_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='club_show',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contest',
            name='school_show',
            field=models.BooleanField(default=False),
        ),
    ]
