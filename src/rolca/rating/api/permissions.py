""".. Ignore pydocstyle D400.

======================
Rating API permissions
======================

.. autoclass:: rolca.rating.api.permissions.IsActiveJudge
    :members:

"""
from django.utils import timezone

from rest_framework import permissions

from rolca.rating.models import Judge


class IsActiveJudge(permissions.BasePermission):
    """Allows access only to active judges."""

    def has_permission(self, request, view):
        """Return `True` if user active judge."""
        return Judge.objects.filter(
            judge=request.user, contest__publish_date__gte=timezone.now()
        ).exists()
