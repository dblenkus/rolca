""".. Ignore pydocstyle D400.

=================
Core API viewsets
=================

.. autoclass:: rolca.core.api.viewsets.PhotoViewSet
    :members:

.. autoclass:: rolca.core.api.viewsets.ContestViewSet
    :members:

"""
from datetime import date
import logging

from django.db.models import Q

from rest_framework import viewsets

from ..models import Photo, Contest
from .permissions import AdminOrReadOnly
from .serializers import PhotoSerializer, ContestSerializer


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PhotoViewSet(viewsets.ModelViewSet):
    """API view Photo objects."""

    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

    def get_queryset(self):
        """Return queryset for photos that can be shown to user.

        Return:
        * all photos for already finished contests
        * user's photos
        """
        return Photo.objects.filter(
            Q(author__user=self.request.user) |
            Q(theme__contest__publish_date__lte=date.today()))


class ContestViewSet(viewsets.ModelViewSet):
    """API view Contest objects."""

    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_classes = (AdminOrReadOnly,)
