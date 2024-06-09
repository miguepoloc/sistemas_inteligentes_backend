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
        unique_together = ['node', 'date_time']


class WeatherStation(BaseModel):
    """
    A class representing a weather station.

    This class inherits from the BaseModel class and provides fields to store various weather data measurements such as
    temperature, dew point, solar radiation, vapor pressure deficit, relative humidity, precipitation, wind speed,
    wind gust, wind direction, solar panel status, battery status, delta T, sun duration, evapotranspiration, and units.

    Fields:
    - date: A DateTimeField that stores the date and time of the weather measurement. It is unique for each instance.
    - temperature: A FloatField that stores the temperature measurement.
    - dew_point: A FloatField that stores the dew point measurement.
    - solar_radiation: An IntegerField that stores the solar radiation measurement.
    - vapor_pressure_deficit: A FloatField that stores the vapor pressure deficit measurement.
    - relative_humidity: A FloatField that stores the relative humidity measurement.
    - precipitation: A FloatField that stores the precipitation measurement.
    - wind_speed: A FloatField that stores the wind speed measurement.
    - wind_gust: A FloatField that stores the wind gust measurement.
    - wind_direction: An IntegerField that stores the wind direction measurement.
    - solar_panel: An IntegerField that stores the status of the solar panel.
    - battery: An IntegerField that stores the status of the battery.
    - delta_t: An IntegerField that stores the delta T measurement.
    - sun_duration: An IntegerField that stores the sun duration measurement.
    - evapotranspiration: A FloatField that stores the evapotranspiration measurement. It can be null.
    - units: A JSONField that stores the units of measurement for each field.

    Meta:
    - db_table: The name of the database table for this model is 'weather_station'.
    - ordering: The default ordering for instances of this model is based on the 'date' field in descending order.
    """

    date = models.DateTimeField(unique=True)
    temperature = models.FloatField()
    dew_point = models.FloatField()
    solar_radiation = models.IntegerField()
    vapor_pressure_deficit = models.FloatField()
    relative_humidity = models.FloatField()
    precipitation = models.FloatField()
    wind_speed = models.FloatField()
    wind_gust = models.FloatField()
    wind_direction = models.IntegerField()
    solar_panel = models.IntegerField()
    battery = models.IntegerField()
    delta_t = models.IntegerField()
    sun_duration = models.IntegerField()
    evapotranspiration = models.FloatField(null=True)
    units = models.JSONField()

    class Meta:
        """
        Meta class for the WeatherStation model.
        """

        db_table = 'weather_station'
        ordering = ['-date']
