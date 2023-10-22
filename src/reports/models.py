"""
File that contains the Django models for the reports app.
"""

from django.db import models

from core.models import BaseModel
from user.models import User


class Visitors(BaseModel):
    """
    A Django model that represents visitor information.

    Fields:
    - ip_visitor: A field to store the visitor's IP address.
    - latitude: A field to store the latitude of the visitor's location.
    - longitude: A field to store the longitude of the visitor's location.
    - city: A field to store the city of the visitor's location.
    - country: A field to store the country of the visitor's location.
    - user: A foreign key to the User model, allowing a visitor to be associated with a user.
    """

    ip_visitor = models.GenericIPAddressField()
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """
        Meta class for the Visitors model.

        Fields:
        - db_table: The name of the database table.
        - ordering: The default ordering of the model.
        """
        db_table = 'visitors'
        ordering = ['-created_at']