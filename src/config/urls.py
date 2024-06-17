"""
File for URL configuration.
"""

import os

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/index.html")),
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls")),
    path("api/auth/", include("authentication.urls")),
    path("api/nodes/", include("nodes.urls")),
    path("api/reports/", include("reports.urls")),
    path("api/ripener/", include("ripener.urls")),
    # Documentation with drf_spectacular swagger
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
CONFIG_SETTINGS = os.getenv("CONFIG_SETTINGS")
if CONFIG_SETTINGS == "config.settings.dev":
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
