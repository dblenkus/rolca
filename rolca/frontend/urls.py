""".. Ignore pydocstyle D400.

=============
Frontend URLs
=============

"""
from django.conf.urls import url

from . import views

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^upload$', views.upload_view, name="upload"),
    url(r'^confirm$', views.confirm_view, name="upload_confirm"),

    # url(r'^seznam$', 'uploader.views.list_select', name="list_select"),
    # url(r'^seznam/(?P<contest_id>\d+)$', 'uploader.views.list_details',
    #     name="list_datails"),

]
