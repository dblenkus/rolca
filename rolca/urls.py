"""Main project's urls."""
from django.urls import include, path

from rest_framework import routers

from rolca.core.api import urls as core_api_urls

route_lists = [core_api_urls.routeList]

router = routers.DefaultRouter()
for route_list in route_lists:
    for prefix, viewset in route_list:
        router.register(prefix, viewset)


urlpatterns = [
    path('api/', include((router.urls, 'rolca-core-api'), namespace='rolca-core-api')),
    path('core/', include('rolca.core.urls', namespace='rolca-core')),
    path('', include('rolca.frontend.urls', namespace='rolca-frontend')),
]
