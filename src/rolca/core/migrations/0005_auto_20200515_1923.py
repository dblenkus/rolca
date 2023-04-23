# Generated by Django 3.0rc1 on 2020-05-15 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_submission_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='submission',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='core.Submission',
            ),
        ),
    ]
