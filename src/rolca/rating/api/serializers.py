""".. Ignore pydocstyle D400.

======================
Rating API serializers
======================

.. autoclass:: rolca.rating.api.serializers.RatingSerializer
    :members:

"""
from rest_framework import exceptions, serializers

from rolca.core.api.serializers import (
    AuthorSerializer as CoreAuthorSerializer,
    BaseSerializer,
    ContestSerializer as CoreContestSerializer,
    FileSerializer,
    SubmissionSerializer as CoreSubmissionSerializer,
    ThemeSerializer as CoreThemeSerializer,
)
from rolca.rating.models import Judge, Rating, SubmissionReward


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
    submissions_number = serializers.SerializerMethodField('get_submissions_number')

    class Meta(CoreThemeSerializer.Meta):
        """Serializer configuration."""

        fields = CoreThemeSerializer.Meta.fields + [
            'ratings_number',
        ]

    def get_ratings_number(self, theme):
        return Rating.objects.filter(
            user=self.context['request'].user, submission__theme=theme
        ).count()

    def get_submissions_number(self, theme):
        return theme.submission_set.filter(submissionset__payment__paid=True).count()


class ContestSerializer(CoreContestSerializer):
    """Serializer for Contest objects."""

    themes = ThemeSerializer(many=True, read_only=True)


class AuthorResultsSerializer(CoreAuthorSerializer):
    """Serializer for Theme objects."""

    reward = serializers.CharField(source='reward.label')
    reward_theme = serializers.CharField(source='reward.theme_id')

    class Meta(CoreAuthorSerializer.Meta):
        """Serializer configuration."""

        fields = CoreAuthorSerializer.Meta.fields + [
            'reward',
            'reward_theme',
        ]


class SubmissionResultsSerializer(CoreSubmissionSerializer):
    accepted = serializers.SerializerMethodField('get_accepted')
    reward_kind = serializers.SerializerMethodField('get_reward_kind')
    reward_label = serializers.CharField(source='reward.label')
    rating = serializers.IntegerField(source='rating_sum')

    class Meta(CoreSubmissionSerializer.Meta):
        """Serializer configuration."""

        fields = CoreSubmissionSerializer.Meta.fields + [
            'accepted',
            'rating',
            'reward_kind',
            'reward_label',
        ]

    def get_fields(self):
        fields = super().get_fields()
        # The field from parent method needs to be overwriten here to tahe the effect.
        fields['files'] = serializers.SerializerMethodField('get_files')
        fields['author'] = AuthorResultsSerializer()

        return fields

    def _is_accepted(self, submission):
        if submission.rating_sum is None:
            return False

        if 'accept_threshold' in self.context:
            return submission.rating_sum >= self.context['accept_threshold']

        return submission.rating_sum >= submission.theme.results.accepted_threshold

    def get_accepted(self, submission):
        return self._is_accepted(submission)

    def get_files(self, submission):
        if not self._is_accepted(submission):
            return None

        return FileSerializer(
            submission.files,
            many=True,
            context={
                'request': self.context['request'],
            },
        ).data

    def get_reward_kind(self, submission):
        mapping = dict(SubmissionReward.KIND_CHOICES)
        if hasattr(submission, 'reward'):
            return mapping[submission.reward.kind]


class ThemeResultsSerializer(CoreThemeSerializer):
    """Serializer for Theme results."""

    submissions = serializers.SerializerMethodField('get_submissions')

    class Meta(CoreThemeSerializer.Meta):
        """Serializer configuration."""

        fields = CoreThemeSerializer.Meta.fields + [
            'submissions',
        ]

    def get_submissions(self, theme):
        return SubmissionResultsSerializer(
            theme.submission_set.all(),
            many=True,
            context={
                'request': self.context['request'],
                'accept_threshold': theme.results.accepted_threshold,
            },
        ).data
