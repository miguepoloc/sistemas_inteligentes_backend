# views.py
import os
import tempfile

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from translate.inference import traducir_audio_arhuaco
from translate.translate_spanish import traducir_audio_espanol


class TraducirAudioView(APIView):
    def post(self, request, format=None):
        audio_file = request.FILES.get("audio")
        language = request.data.get("language")

        if not audio_file or not language:
            return Response({"error": "Debe enviar 'audio' y 'language'."},
                            status=status.HTTP_400_BAD_REQUEST)

        if language not in ["es", "arh"]:
            return Response({"error": "El campo 'language' debe ser 'es' o 'arh'."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Guardar audio temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            if language == "es":
                resultado = traducir_audio_espanol(tmp_path)
            else:
                resultado = traducir_audio_arhuaco(tmp_path)
        finally:
            os.unlink(tmp_path)

        return Response(resultado, status=status.HTTP_200_OK)
