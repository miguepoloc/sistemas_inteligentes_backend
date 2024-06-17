"""
File with serializers for the nodes app.
"""

# from datetime import datetime
# from typing import Union

# from django.core.files.uploadedfile import UploadedFile
# from django.utils import timezone
from rest_framework import serializers

from ripener.models import MachineInfo, NodesInfo


class MachineSerializer(serializers.ModelSerializer):
    """
    A Django REST Framework serializer for the Nodes model.
    """

    class Meta:
        """
        Meta class for the NodesSerializer.
        """

        model = MachineInfo
        fields = '__all__'


class NodesSerializer(serializers.ModelSerializer):
    """
    A Django REST Framework serializer for the NodesStorage model.
    """

    class Meta:
        """
        Meta class for the NodesStorageSerializer.
        """

        model = NodesInfo
        fields = '__all__'
