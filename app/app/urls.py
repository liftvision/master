__version__ = "0.1.0"
__author__ = "김동주 <hepheir@gmail.com>"

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import lift.urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include([
        path("token/", include([
            path("", TokenObtainPairView.as_view(), name="token_obtain_pair"),
            path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        ])),
        path("ev/", include(lift.urls.urlpatterns)),
    ])),
    path("schema/", include([
        path("", SpectacularAPIView.as_view(), name="schema"),
        path("swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ])),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
