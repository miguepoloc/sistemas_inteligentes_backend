"""
File that contains the Django models for the nodes app.
"""

from django.db import models

from core.models import BaseModel


class Nodes(BaseModel):
    """
    A Django model that represents nodes in a system.

    Fields:
    - name (str): The name of the node.
    - type (str): The type of the node (master or worker).
    - description (str, optional): A description of the node.
    - latitude (float): The latitude of the node's location.
    - longitude (float): The longitude of the node's location.
    """

    CHOICES = (
        ('master', 'Master'),
        ('worker', 'Worker'),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=CHOICES)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        """
        Meta class for the Nodes model.
        """

        db_table = 'nodes'

    def __str__(self):
        """
        Returns a string representation of the node's name.
        """
        return self.name


class NodesStorage(BaseModel):
    """
    A Django model that represents a storage table for node data.

    Fields:
    - node: A foreign key to the Nodes model, representing the associated node.
    - date_time: A DateTimeField representing the date and time of the data.
    - temperature: A DecimalField representing the temperature value.
    - humidity: A DecimalField representing the humidity value.
    - pressure: A DecimalField representing the pressure value.
    - altitude: A DecimalField representing the altitude value.
    """

    node = models.ForeignKey(Nodes, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    pressure = models.DecimalField(max_digits=5, decimal_places=2)
    altitude = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        """
        Meta class for the NodesStorage model.
        """

        db_table = 'nodes_storage'
        ordering = ['-date_time']
