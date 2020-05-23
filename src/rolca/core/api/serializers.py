""".. Ignore pydocstyle D400.

====================
Core API serializers
====================

.. autoclass:: rolca.core.api.serializers.FileSerializer
    :members:

.. autoclass:: rolca.core.api.serializers.PhotoSerializer
    :members:

.. autoclass:: rolca.core.api.serializers.ThemeSerializer
    :members:

.. autoclass:: rolca.core.api.serializers.ContestSerializer
    :members:

"""
from rest_framework import serializers

from rolca.core.models import Contest, File, Submission, Theme


class BaseSerializer(serializers.ModelSerializer):
    """Base serializer for Rolca models."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """Serializer configuration."""

        fields = ['id', 'user']
        read_only_fields = ['id']


class FileSerializer(BaseSerializer):
    """Serializer for File objects."""

    class Meta(BaseSerializer.Meta):
        """Serializer configuration."""

        model = File
        fields = BaseSerializer.Meta.fields + ['file']


class SubmissionSerializer(BaseSerializer):
    """Serializer for Submission objects."""

    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(),)

    class Meta(BaseSerializer.Meta):
        """Serializer configuration."""

        model = Submission
        fields = BaseSerializer.Meta.fields + ['author', 'theme', 'title', 'files']


class ThemeSerializer(BaseSerializer):
    """Serializer for Theme objects."""

    class Meta(BaseSerializer.Meta):
        """Serializer configuration."""

        model = Theme
        fields = BaseSerializer.Meta.fields + ['title', 'is_series', 'n_photos']


class ContestSerializer(BaseSerializer):
    """Serializer for Contest objects."""

    themes = ThemeSerializer(many=True, read_only=True)

    class Meta(BaseSerializer.Meta):
        """Serializer configuration."""

        model = Contest
        fields = BaseSerializer.Meta.fields + [
            'title',
            'start_date',
            'end_date',
            'themes',
        ]
