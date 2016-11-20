# -*- coding: utf-8 -*-
from datetime import date
import json
import logging
import os

from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseForbidden,
    HttpResponseNotAllowed)
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from rest_framework import viewsets

from .forms import ThemeFormSet
from .models import File, Photo, Salon, Theme, Author
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


class UploadView(FormView):
    template_name = 'uploader/upload.html'
    form_class = ThemeFormSet
    success_url = reverse_lazy('upload_confirm')

    def form_valid(self, form_set):
        author = None
        for form in form_set:
            # validation is skipped for empty forms in formset, so we
            # have to check that there are actual data to save
            if form.cleaned_data:
                if not author:
                    author = Author.objects.create(
                        uploader=self.request.user,
                        first_name=self.request.user.first_name,
                        last_name=self.request.user.last_name,
                    )
                    # XXX: This must be determined in proper way
                    theme = Theme.objects.last()
                form.save(self.request.user, author, theme)
        return super(UploadView, self).form_valid(form_set)

upload_view = login_required(UploadView.as_view())
confirm_view = TemplateView.as_view(template_name='uploader/upload_confirm.html')


def list_select(request):
    salons = Salon.objects.all()

    response = {'salons': salons}
    return render(request, os.path.join('uploader', 'list_select.html'),
                  response)


def list_details(request, salon_id):
    salon = get_object_or_404(Salon, pk=salon_id)
    themes = Theme.objects.filter(salon=salon)

    response = {'users': []}
    # for user in Profile.objects.all():  # pylint: disable=no-member
    #     count = Photo.objects.filter(theme__in=themes, user=user).count()
    #     if count > 0:
    #         response['users'].append({
    #             'name': user.get_short_name,
    #             'school': user.school,
    #             'count': count})

    response['salon'] = salon
    return render(request, os.path.join('uploader', 'list_details.html'),
                  response)


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
