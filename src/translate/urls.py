# urls.py
from django.urls import path

from translate.views import TraducirAudioView

urlpatterns = [
    path("traducir-audio/", TraducirAudioView.as_view(), name="traducir-audio"),
]
