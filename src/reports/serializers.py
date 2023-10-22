"""
File with serializers for the reports app.
"""

from rest_framework import serializers

from reports.models import Visitors


class VisitorsSerializer(serializers.ModelSerializer):
    """
    A Django REST Framework serializer for the Visitors model.
    """

    class Meta:
        """
        Meta class for the VisitorsSerializer.
        """

        model = Visitors
        fields = '__all__'


    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)