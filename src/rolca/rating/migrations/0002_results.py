# Generated by Django 3.0rc1 on 2020-11-22 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0019_submission_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemeResults',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('accepted_threshold', models.SmallIntegerField()),
                (
                    'theme',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='results',
                        to='core.Theme',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubmissionReward',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                (
                    'kind',
                    models.SmallIntegerField(
                        choices=[
                            (1, 'Gold'),
                            (2, 'Silver'),
                            (3, 'Bronze'),
                            (4, 'Honorable Mention'),
                        ]
                    ),
                ),
                (
                    'submission',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reward',
                        to='core.Submission',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
