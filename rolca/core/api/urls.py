""".. Ignore pydocstyle D400.

===================
Rolca core api urls
===================

The ``routList`` is ment to be included in ``urlpatterns`` with the
following code:

.. code-block:: python

    from rest_framework import routers

    from rolca.core.api import urls as core_api_urls

    route_lists = [
        core_api_urls.routeList,
        ...
    ]

    router = routers.DefaultRouter()
    for route_list in route_lists:
        for prefix, viewset in route_list:
            router.register(prefix, viewset)

For advanced configuration code can be accordingly changed to meet the
needs.

"""
from .viewsets import PhotoViewSet, SalonViewSet


routeList = (  # pylint: disable=invalid-name
    (r'photo', PhotoViewSet),
    (r'salon', SalonViewSet),
)
