# Generated by Django 3.0.2 on 2020-02-18 16:41

from django.db import migrations, models
import django.db.models.deletion


def move_submission_file(apps, schema_editor):
    """Move relation between Submission and File models to later one."""
    File = apps.get_model("core", "File")

    for file in File.objects.all():
        file.submission = file.submission_old
        file.save()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_theme_is_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='submission',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='core.Submission',
            ),
        ),
        migrations.AlterField(
            model_name='submission',
            name='photo',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='submission_old',
                to='core.File',
            ),
        ),
        migrations.RunPython(move_submission_file),
        migrations.RemoveField(
            model_name='submission',
            name='photo',
        ),
        migrations.AlterField(
            model_name='file',
            name='submission',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to='core.Submission'
            ),
        ),
    ]
