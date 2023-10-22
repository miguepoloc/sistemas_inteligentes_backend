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

    def validate(self, attrs: dict) -> dict:
        """
        Validate the data before creating a new visitor.

        Args:
            attrs (dict): The data to validate.

        Returns:
            dict: The validated data.
        """
        return super().validate(attrs)

    def create(self, validated_data: dict) -> Visitors:
        """
        Create a new visitor.

        Args:
            validated_data (dict): The validated data.

        Returns:
            Visitors: The newly created visitor.
        """
        return super().create(validated_data)
