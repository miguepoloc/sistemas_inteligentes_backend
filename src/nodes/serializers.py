"""
File with serializers for the nodes app.
"""

from rest_framework import serializers

from nodes.models import Nodes, NodesStorage


class NodesSerializer(serializers.ModelSerializer):
    """
    A Django REST Framework serializer for the Nodes model.
    """

    class Meta:
        """
        Meta class for the NodesSerializer.
        """

        model = Nodes
        fields = '__all__'


class NodesStorageSerializer(serializers.ModelSerializer):
    """
    A Django REST Framework serializer for the NodesStorage model.
    """

    class Meta:
        """
        Meta class for the NodesStorageSerializer.
        """

        model = NodesStorage
        fields = '__all__'
