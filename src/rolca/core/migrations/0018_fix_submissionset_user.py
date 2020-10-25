# Generated by Django 3.0rc1 on 2020-10-25 17:22

from django.db import migrations


def update_submission_sets(apps, schema_editor):
    """Fix user field on SubmissionSet objects."""
    SubmissionSet = apps.get_model("core", "SubmissionSet")

    for submission_set in SubmissionSet.objects.all():
        submission = submission_set.submissions.first()
        if not submission:
            continue
        else:
            submission_set.user = submission.user
            submission_set.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_enlarge_thumbnails'),
    ]

    operations = [
        migrations.RunPython(update_submission_sets),
    ]