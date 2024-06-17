""" models of the ripener app """

from django.db import models

from core.models import BaseModel


class MachineInfo(BaseModel):

    rod_set = models.DecimalField(max_digits=10, decimal_places=2)
    flow_pump = models.DecimalField(max_digits=10, decimal_places=2)
    time_start = models.DateTimeField()
    time_on = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        """
        Meta class for the machine.
        """

        db_table = 'machine_info'


class NodesInfo(BaseModel):

    node = models.ForeignKey(MachineInfo, on_delete=models.CASCADE)
    temperature_rod = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    temperature_environment = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    humidity_environment = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    concentration_c2h4 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    concentration_ozone = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    info_extra = models.JSONField(null=True)
    id_node = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """
        Meta class for the NodesStorage model.
        """

        db_table = 'nodes_info'
