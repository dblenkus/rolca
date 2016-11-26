"""Test project's urls."""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from rest_framework import routers

from rolca.core.api import urls as core_api_urls


route_lists = [  # pylint: disable=invalid-name
    core_api_urls.routeList
]

router = routers.DefaultRouter()  # pylint: disable=invalid-name
for route_list in route_lists:
    for prefix, viewset in route_list:
        router.register(prefix, viewset)


urlpatterns = [  # pylint: disable=invalid-name
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^api/', include(router.urls, namespace='rolca-core-api')),

    url(r'^', include('rolca.frontend.urls', namespace='rolca-frontend')),
]
