import os

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='api-docs'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/auth/', include('dj_rest_auth.urls')),
]

CONFIG_SETTINGS = os.getenv("CONFIG_SETTINGS")
if CONFIG_SETTINGS == "config.settings.local":
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
