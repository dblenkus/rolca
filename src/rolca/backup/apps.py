"""Application configuration."""
from django.apps import AppConfig


class RolcaBackupConfig(AppConfig):
    """Application configuration."""

    name = 'rolca.backup'
    verbose_name = "Rolca Backup"

    def ready(self):
        """Application initialization."""
        # Register signals handlers
        from . import signals  # noqa: F401
