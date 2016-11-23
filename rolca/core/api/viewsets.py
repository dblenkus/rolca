"""Rolca core API viewsets."""
from datetime import date
import logging

from django.db.models import Q

from rest_framework import viewsets

from ..models import Photo, Salon
from .permissions import AdminOrReadOnly
from .serializers import PhotoSerializer, SalonSerializer


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PhotoViewSet(viewsets.ModelViewSet):
    """API view Photo objects."""

    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

    def get_queryset(self):
        """Return queryset for photos that can be shown to user.

        Return:
        * all photos for already finished salons
        * photos of tha salons where user is in a jury
        * user's photos
        """
        return Photo.objects.filter(
            Q(author__uploader=self.request.user) |
            Q(theme__salon__results_date__lte=date.today()) |
            Q(theme__salon__judges=self.request.user))


class SalonViewSet(viewsets.ModelViewSet):
    """API view Salon objects."""

    queryset = Salon.objects.all()
    serializer_class = SalonSerializer
    permission_classes = (AdminOrReadOnly,)
