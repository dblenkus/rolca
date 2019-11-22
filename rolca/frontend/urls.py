""".. Ignore pydocstyle D400.

=============
Frontend URLs
=============

"""
from django.urls import path
from django.views.generic.base import RedirectView

from rolca.frontend import views

app_name = 'rolca-frontend'
urlpatterns = [  # pylint: disable=invalid-name
    path('upload/', views.select_contest_view, name="select_contest"),
    path('upload/<int:contest_id>', views.upload_view, name="upload"),
    path('confirm', views.confirm_view, name="upload_confirm"),
    path('', RedirectView.as_view(pattern_name='rolca-frontend:select_contest')),

    # path('seznam', 'uploader.views.list_select', name="list_select"),
    # path('seznam/<int:contest_id>', 'uploader.views.list_details', name="list_datails"),

]
