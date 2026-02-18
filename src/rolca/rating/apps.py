"""Application configuration."""
from django.apps import AppConfig


class RolcaRatingConfig(AppConfig):
    """Application configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rolca.rating'
    verbose_name = "Rolca rating"
