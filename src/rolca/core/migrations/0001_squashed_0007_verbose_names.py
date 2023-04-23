# Generated by Django 3.0.2 on 2020-01-03 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rolca.core.models


class Migration(migrations.Migration):
    replaces = [
        ('core', '0001_initial'),
        ('core', '0002_add_contest_description'),
        ('core', '0003_contest_login_required'),
        ('core', '0004_author_email'),
        ('core', '0005_nonrequired_user'),
        ('core', '0006_photo_title_not_required'),
        ('core', '0007_verbose_names'),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
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
                    'first_name',
                    models.CharField(max_length=30, verbose_name='First name'),
                ),
                (
                    'last_name',
                    models.CharField(max_length=30, verbose_name='Last name'),
                ),
                (
                    'mentor',
                    models.CharField(
                        blank=True, max_length=60, null=True, verbose_name='Mentor'
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
                (
                    'email',
                    models.EmailField(
                        blank=True, max_length=254, null=True, verbose_name='Email'
                    ),
                ),
            ],
            options={
                'abstract': False,
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
            },
        ),
        migrations.CreateModel(
            name='Contest',
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
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('start_date', models.DateTimeField(verbose_name='Start date')),
                ('end_date', models.DateTimeField(verbose_name='End date')),
                (
                    'publish_date',
                    models.DateTimeField(blank=True, verbose_name='Publish date'),
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
                (
                    'description',
                    models.TextField(blank=True, null=True, verbose_name='Description'),
                ),
                (
                    'login_required',
                    models.BooleanField(default=False, verbose_name='Login required'),
                ),
            ],
            options={
                'abstract': False,
                'verbose_name': 'contest',
                'verbose_name_plural': 'contests',
            },
        ),
        migrations.CreateModel(
            name='File',
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
                    'file',
                    models.ImageField(
                        upload_to=rolca.core.models.generate_file_filename
                    ),
                ),
                (
                    'thumbnail',
                    models.ImageField(
                        upload_to=rolca.core.models.generate_thumb_filename
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
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
            },
        ),
        migrations.CreateModel(
            name='Theme',
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
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('n_photos', models.IntegerField(verbose_name='Number of photos')),
                (
                    'contest',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='themes',
                        to='core.Contest',
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
                'verbose_name': 'theme',
                'verbose_name_plural': 'themes',
            },
        ),
        migrations.CreateModel(
            name='Photo',
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
                    'title',
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name='Title'
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='core.Author'
                    ),
                ),
                (
                    'photo',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to='core.File'
                    ),
                ),
                (
                    'theme',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to='core.Theme'
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
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
            },
        ),
    ]
