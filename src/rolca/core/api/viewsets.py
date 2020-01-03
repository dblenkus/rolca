""".. Ignore pydocstyle D400.

=================
Core API viewsets
=================

.. autoclass:: rolca.core.api.viewsets.PhotoViewSet
    :members:

.. autoclass:: rolca.core.api.viewsets.ContestViewSet
    :members:

"""
import logging
from datetime import date

from django.db.models import Q

from rest_framework import viewsets

from rolca.core.api.permissions import AdminOrReadOnly
from rolca.core.api.serializers import ContestSerializer, SubmissionSerializer
from rolca.core.models import Contest, Submission

logger = logging.getLogger(__name__)


class SubmissionViewSet(viewsets.ModelViewSet):
    """API view Submission objects."""

    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def get_queryset(self):
        """Return queryset for submissions that can be shown to user.

        Return:
        * all submissions for already finished contests
        * user's submissions

        """
        return Submission.objects.filter(
            Q(author__user=self.request.user)
            | Q(theme__contest__publish_date__lte=date.today())
        )


class ContestViewSet(viewsets.ModelViewSet):
    """API view Contest objects."""

    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_classes = (AdminOrReadOnly,)
