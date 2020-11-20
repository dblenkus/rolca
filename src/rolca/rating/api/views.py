""".. Ignore pydocstyle D400."""
from django.utils import timezone

from rest_framework import mixins, permissions, viewsets

from rolca.core.api.serializers import SubmissionSerializer
from rolca.core.api.filters import ContestFilter, SubmissionFilter
from rolca.core.models import Contest, Submission, Theme
from rolca.rating.api.filters import RatingFilter
from rolca.rating.api.permissions import IsActiveJudge
from rolca.rating.api.serializers import ContestSerializer, RatingSerializer
from rolca.rating.models import Judge, Rating


class RatingViewSet(viewsets.ModelViewSet):
    """API viewset for Rating objects."""

    queryset = Rating.objects.none()
    serializer_class = RatingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = RatingFilter

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)


class SubmissionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filter_class = SubmissionFilter
    permission_classes = (IsActiveJudge,)

    def get_queryset(self):
        """Return queryset for submissions that can be shown to judge."""
        judge_qs = Judge.objects.filter(judge=self.request.user)
        theme_qs = Theme.objects.filter(
            contest__in=judge_qs.values('contest'),
            contest__publish_date__gte=timezone.now(),
        )
        return Submission.objects.filter(
            theme__in=theme_qs,
            submissionset__payment__paid=True,
        )


class ContestViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    filter_class = ContestFilter
    permission_classes = (IsActiveJudge,)

    def get_queryset(self):
        """Return queryset for contests that can be shown to judge."""
        judge_qs = Judge.objects.filter(judge=self.request.user)
        return Contest.objects.filter(
            pk__in=judge_qs.values('contest'),
            publish_date__gte=timezone.now(),
        )
