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

from rolca.core.models import Author, Contest, File, Submission, Theme


class BaseSerializer(serializers.ModelSerializer):
    """Base serializer for Rolca models."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """Serializer configuration."""

        fields = ['id', 'user']
        read_only_fields = ['id']


class IdRelatedSerializer(serializers.Serializer):
    """Serializer for File objects."""

    id = serializers.IntegerField()


class FileSerializer(BaseSerializer):
    """Serializer for File objects."""

    class Meta(BaseSerializer.Meta):
        """Serializer configuration."""

        model = File
        fields = BaseSerializer.Meta.fields + ['file']


class AuthorSerializer(BaseSerializer):
    """Serializer for Author objects."""

    class Meta(BaseSerializer.Meta):
        """Serializer configuration."""

        model = Author
        fields = BaseSerializer.Meta.fields + ['first_name', 'last_name', 'email']


class SubmissionSerializer(BaseSerializer):
    """Serializer for Submission objects."""

    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(),)

    class Meta(BaseSerializer.Meta):
        """Serializer configuration."""

        model = Submission
        fields = BaseSerializer.Meta.fields + ['author', 'theme', 'title', 'files']

    def get_fields(self):
        """Dynamically adapt fields based on the current request."""
        fields = super().get_fields()

        if self.context['request'].method == "GET":
            fields['author'] = AuthorSerializer()
            fields['files'] = FileSerializer(many=True)
        else:
            fields['author'] = IdRelatedSerializer()
            fields['files'] = IdRelatedSerializer(many=True)

        return fields

    def validate_files(self, value):
        file_ids = [file['id'] for file in value]
        return File.objects.filter(id__in=file_ids)

    def validate_author(self, value):
        return Author.objects.get(pk=value['id'])

    def create(self, validated_data):
        files = validated_data.pop('files')
        submission = Submission.objects.create(**validated_data)
        submission.files.add(*files)
        return submission


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
            'description',
            'start_date',
            'end_date',
            'themes',
            'header_image',
            'notice_html',
        ]
