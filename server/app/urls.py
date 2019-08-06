from django.urls import path, include

from .api.v1 import urls

urlpatterns = [
    path("api/v1/", include(urls))
]