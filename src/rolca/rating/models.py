""".. Ignore pydocstyle D400.

=============
Rating models
=============

.. autoclass:: rolca.rating.models.Judge
    :members:

.. autoclass:: rolca.rating.models.Rating
    :members:

"""
from django.conf import settings
from django.db import models

from rolca.core.models import BaseModel, Contest, Submission, Theme


class Judge(BaseModel):
    """Model for assigning judges to contests."""

    contest = models.ForeignKey(
        Contest, on_delete=models.CASCADE, related_name='judges'
    )

    judge = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+'
    )


class Rating(BaseModel):
    """Model for rating submissions"""

    judge = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name='ratings')

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

    rating = models.IntegerField()


class ThemeResults(BaseModel):
    """Model for theme results."""

    theme = models.OneToOneField(
        Theme, on_delete=models.CASCADE, related_name='results'
    )

    accepted_threshold = models.SmallIntegerField()


class SubmissionReward(BaseModel):
    """Model for submission rewards."""

    GOLD = 1
    SILVER = 2
    BRONZE = 3
    HONORABLE_MENTION = 4
    KIND_CHOICES = [
        (GOLD, 'Gold'),
        (SILVER, 'Silver'),
        (BRONZE, 'Bronze'),
        (HONORABLE_MENTION, 'Honorable Mention'),
    ]

    submission = models.OneToOneField(
        Submission, on_delete=models.CASCADE, related_name='reward'
    )

    kind = models.SmallIntegerField(choices=KIND_CHOICES)
