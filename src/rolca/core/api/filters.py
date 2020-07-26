""".. Ignore pydocstyle D400.

==============
Core API views
==============

"""
from django_filters import rest_framework as filters

from rolca.core.models import Submission


class SubmissionFilter(filters.FilterSet):
    """Filter for Submission API endpoint."""

    contest = filters.CharFilter(field_name="theme__contest")

    class Meta:
        model = Submission
        fields = ["theme"]
