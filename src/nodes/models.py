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
    - humidity_hd38: A DecimalField representing the humidity_hd38 value.
    - humidity_soil: A DecimalField representing the humidity_soil value.
    - temperature_soil: A DecimalField representing the temperature_soil value.
    - conductivity_soil: A DecimalField representing the conductivity_soil value.
    - ph_soil: A DecimalField representing the ph_soil value.
    - nitrogen_soil: A DecimalField representing the nitrogen_soil value.
    - phosphorus_soil: A DecimalField representing the phosphorus_soil value.
    - potassium_soil: A DecimalField representing the potassium_soil value.
    - battery_level: A DecimalField representing the battery_level value.
    """

    node = models.ForeignKey(Nodes, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    temperature = models.DecimalField(max_digits=10, decimal_places=2)
    humidity = models.DecimalField(max_digits=10, decimal_places=2)
    pressure = models.DecimalField(max_digits=10, decimal_places=2)
    altitude = models.DecimalField(max_digits=10, decimal_places=2)
    humidity_hd38 = models.DecimalField(max_digits=10, decimal_places=2)
    humidity_soil = models.DecimalField(max_digits=10, decimal_places=2)
    temperature_soil = models.DecimalField(max_digits=10, decimal_places=2)
    conductivity_soil = models.DecimalField(max_digits=10, decimal_places=2)
    ph_soil = models.DecimalField(max_digits=10, decimal_places=2)
    nitrogen_soil = models.DecimalField(max_digits=10, decimal_places=2)
    phosphorus_soil = models.DecimalField(max_digits=10, decimal_places=2)
    potassium_soil = models.DecimalField(max_digits=10, decimal_places=2)
    battery_level = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        """
        Meta class for the NodesStorage model.
        """

        db_table = 'nodes_storage'
        ordering = ['-date_time']
