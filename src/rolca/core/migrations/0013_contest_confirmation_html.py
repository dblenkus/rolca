# Generated by Django 3.0rc1 on 2020-10-21 10:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0012_submissionset_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='confirmation_html',
            field=models.TextField(default=''),
        ),
    ]
