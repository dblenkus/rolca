# Generated by Django 3.0rc1 on 2020-06-09 19:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0008_auto_20200609_1748'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={
                'ordering': ['id'],
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
            },
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={
                'ordering': ['id'],
                'verbose_name': 'contest',
                'verbose_name_plural': 'contests',
            },
        ),
        migrations.AlterModelOptions(
            name='file',
            options={
                'ordering': ['id'],
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
            },
        ),
        migrations.AlterModelOptions(
            name='submission',
            options={
                'ordering': ['id'],
                'verbose_name': 'submission',
                'verbose_name_plural': 'submissions',
            },
        ),
        migrations.AlterModelOptions(
            name='theme',
            options={
                'ordering': ['id'],
                'verbose_name': 'theme',
                'verbose_name_plural': 'themes',
            },
        ),
    ]
