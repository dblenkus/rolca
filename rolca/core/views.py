# -*- coding: utf-8 -*-
from datetime import date
import json
import logging
import os

from django.db.models import Q
from django.conf import settings
from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed)
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets

from .models import File, Photo, Salon, Theme
from .permissions import AdminOrReadOnly
from .serializers import PhotoSerializer, SalonSerializer
# from login.models import Profile


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(
            Q(participent__uploader=self.request.user) |
            Q(theme__salon__results_date__lte=date.today()) |
            Q(theme__salon__judges=self.request.user))


class SalonViewSet(viewsets.ModelViewSet):
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer
    permission_classes = (AdminOrReadOnly,)


@csrf_exempt
def upload(request):
    if request.method != 'POST':
        logger.warning("Upload request other than POST.")
        return HttpResponseNotAllowed(['POST'], 'Only POST accepted')

    if not request.user.is_authenticated():
        logger.warning('Anonymous user tried to upload file.')
        return HttpResponseForbidden('Please login!')

    if request.FILES is None:
        logger.warning("Upload request without attached image.")
        return HttpResponseBadRequest('Must have files attached!')

    fn = request.FILES[u'files[]']
    logger.info("Image received.")

    file_ = File(file=fn, user=request.user)

    if file_.file.size > settings.MAX_UPLOAD_SIZE:
        logger.warning("Too big file.")
        return HttpResponseBadRequest("File can't excede size of {}KB".format(
            settings.MAX_UPLOAD_SIZE / 1024))

    max_image_resolution = settings.MAX_IMAGE_RESOLUTION
    if max(file_.file.width, file_.file.height) > max_image_resolution:
        logger.warning("Too big file.")
        return HttpResponseBadRequest("File can't excede size of {}px".format(
            settings.MAX_IMAGE_RESOLUTION))

    file_.save()

    result = []
    result.append({"name": os.path.basename(file_.file.name),
                   "size": file_.file.size,
                   "url": file_.file.url,
                   "thumbnail": file_.thumbnail.url,  # pylint: disable=no-member
                   "delete_url": '',
                   "delete_type": "POST"})
    response_data = json.dumps(result)
    return HttpResponse(response_data, content_type='application/json')