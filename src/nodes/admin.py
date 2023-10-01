"""
File contains admin configuration for nodes app.
"""

from django.contrib import admin

from nodes.models import Nodes, NodesStorage


class NodesAdmin(admin.ModelAdmin):
    """
    A Django ModelAdmin class for the Nodes model.
    """

    list_display = ('name', 'type', 'description', 'latitude', 'longitude')
    list_filter = ('type',)
    search_fields = ('name', 'type', 'description', 'latitude', 'longitude')


class NodesStorageAdmin(admin.ModelAdmin):
    """
    A Django ModelAdmin class for the NodesStorage model.
    """

    list_display = ('node', 'date_time', 'temperature', 'humidity', 'pressure', 'altitude')
    list_filter = ('node',)
    search_fields = ('node', 'date_time', 'temperature', 'humidity', 'pressure', 'altitude')


admin.site.register(Nodes, NodesAdmin)
admin.site.register(NodesStorage, NodesStorageAdmin)
