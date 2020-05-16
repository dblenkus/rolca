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


class FileSerializer(serializers.ModelSerializer):
    """Serializer for File objects."""

    class Meta:
        """Serializer configuration."""

        model = File
        fields = (
            'id',
            'file',
        )
        read_only_fields = ['id']


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer for Submission objects."""

    photo = FileSerializer()

    class Meta:
        """Serializer configuration."""

        model = Submission
        fields = ('id', 'photo', 'title')


class ThemeSerializer(serializers.ModelSerializer):
    """Serializer for Theme objects."""

    class Meta:
        """Serializer configuration."""

        model = Theme
        fields = ('id', 'title', 'is_series', 'n_photos')


class ContestSerializer(serializers.ModelSerializer):
    """Serializer for Contest objects."""

    themes = ThemeSerializer(many=True, read_only=True)

    class Meta:
        """Serializer configuration."""

        model = Contest
        fields = ('id', 'title', 'start_date', 'end_date', 'themes')
