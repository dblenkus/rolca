""".. Ignore pydocstyle D400.

======================
Rating API serializers
======================

.. autoclass:: rolca.rating.api.serializers.RatingSerializer
    :members:

"""
from rest_framework import exceptions, serializers

from rolca.core.api.serializers import (
    BaseSerializer,
    ContestSerializer as CoreContestSerializer,
    ThemeSerializer as CoreThemeSerializer,
)
from rolca.rating.models import Judge, Rating


class RatingSerializer(BaseSerializer):
    """Serializer for Rating objects."""

    class Meta(BaseSerializer.Meta):
        """Serializer configuration."""

        model = Rating
        fields = BaseSerializer.Meta.fields + ['submission', 'rating']

    def create(self, validated_data):
        submission = validated_data.pop('submission')
        try:
            user = self.context['request'].user
            judge = Judge.objects.get(judge=user, contest=submission.theme.contest)
        except Judge.DoesNotExist:
            raise exceptions.NotAuthenticated(
                "You don't have permission to rate this contest."
            )

        rating, _ = Rating.objects.update_or_create(
            submission=submission, judge=judge, defaults=validated_data
        )

        return rating


class ThemeSerializer(CoreThemeSerializer):
    """Serializer for Theme objects."""

    ratings_number = serializers.SerializerMethodField('get_ratings_number')

    class Meta(CoreThemeSerializer.Meta):
        """Serializer configuration."""

        fields = CoreThemeSerializer.Meta.fields + [
            'ratings_number',
        ]

    def get_ratings_number(self, theme):
        return Rating.objects.filter(
            user=self.context['request'].user, submission__theme=theme
        ).count()


class ContestSerializer(CoreContestSerializer):
    """Serializer for Contest objects."""

    themes = ThemeSerializer(many=True, read_only=True)
