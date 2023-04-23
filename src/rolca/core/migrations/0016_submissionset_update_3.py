# Generated by Django 3.0rc1 on 2020-10-22 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0015_submissionset_update_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionset',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='core.Author'
            ),
        ),
        migrations.AlterField(
            model_name='submissionset',
            name='contest',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='submission_sets',
                to='core.Contest',
            ),
        ),
    ]
