"""Rolca frontend context processors."""

from django.conf import settings


def ui_configuration(request):
    """Set parameters for configuring UI."""
    return {
        'materialize_color': getattr(settings, 'ROLCA_FRONTEND_COLOR', 'orange'),
        'frontend_title': getattr(settings, 'ROLCA_FRONTEND_TITLE', 'Rolca'),
    }
