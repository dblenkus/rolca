from django.conf.urls import url
from django.views.generic import TemplateView

from . import views as core_views

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^$', core_views.upload_app, name="upload_app"),
    url(r'^potrditev$',
        TemplateView.as_view(template_name='uploader/upload_confirm.html'),
        name="upload_confirm"),

    # url(r'^seznam$', 'uploader.views.list_select', name="list_select"),
    # url(r'^seznam/(?P<salon_id>\d+)$', 'uploader.views.list_details',
    #     name="list_datails"),

    # url(r'^razpisi$',
    #     TemplateView.as_view(template_name="uploader/notices.html"),
    #     name="notices"),
    # url(r'^razpisi/os$',
    #     TemplateView.as_view(template_name="uploader/notice_os.html"),
    #     name="notice_os"),
    # url(r'^razpisi/ss$',
    #     TemplateView.as_view(template_name="uploader/notice_ss.html"),
    #     name="notice_ss"),

]
