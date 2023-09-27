"""
File with configuration for the nodes app.
"""

from django.apps import AppConfig


class NodesConfig(AppConfig):
    """
    A Django AppConfig class for the nodes app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nodes'
