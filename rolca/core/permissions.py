"""Rolca permissions."""
from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Permission class for DRF."""

    def has_permission(self, request, view):
        """Return `True` if method is safe or user is superuser."""
        return(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )
