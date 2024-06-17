"""
File that contains the urls of the nodes app.
"""

from django.urls import path

from ripener.views import MachineView, NodesView

app_name = 'ripener'  # pylint: disable=C0103

urlpatterns: list = [
    path('', MachineView.as_view(), name='machine_list'),
    path('nodes/', NodesView.as_view(), name='nodes_detail'),
]
