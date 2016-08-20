from django.conf.urls import include, url
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^accounts/login/$', auth_views.login),

    url(r'^', include('rolca_core.urls')),
]
