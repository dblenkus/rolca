from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('rolca_core.urls')),
]