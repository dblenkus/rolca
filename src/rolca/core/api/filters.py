""".. Ignore pydocstyle D400.

==============
Core API views
==============

"""
from django_filters import rest_framework as filters

from django.utils import timezone

from rolca.core.models import Contest, Submission


class SubmissionFilter(filters.FilterSet):
    """Filter for Submission API endpoint."""

    contest = filters.CharFilter(field_name="theme__contest")

    class Meta:
        model = Submission
        fields = ["theme"]


class ContestFilter(filters.FilterSet):
    """Filter for Contest API endpoint."""

    def filter_is_active(self, queryset, name, value):
        """Return active contests."""
        now = timezone.now()
        filters = {'start_date__lte': now, 'end_date__gte': now}
        return queryset.filter(**filters) if value else queryset.exclude(**filters)

    def filter_submitted(self, queryset, name, value):
        """Return contests to which current user has submitted to."""
        if self.request.user.is_anonymous:
            return queryset.none() if value else queryset

        filters = {'themes__submission__user': self.request.user}
        return queryset.filter(**filters) if value else queryset.exclude(**filters)

    is_active = filters.BooleanFilter(method="filter_is_active")
    submitted = filters.BooleanFilter(method="filter_submitted")
