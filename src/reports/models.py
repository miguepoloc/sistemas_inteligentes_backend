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
    - ip_address: A field to store the visitor's IP address.
    - user: A foreign key to the User model, allowing a visitor to be associated with a user.
    """

    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    page = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        """
        Meta class for the Visitors model.

        Fields:
        - db_table: The name of the database table.
        """

        db_table = 'visitors'
