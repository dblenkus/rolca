from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('rolca_core.urls')),
]
