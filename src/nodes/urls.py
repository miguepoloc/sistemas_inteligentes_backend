"""
File that contains the urls of the nodes app.
"""

from django.urls import path

from nodes.views import NodesStorageView, NodesView, WeatherStationView

app_name = 'nodes'  # pylint: disable=C0103

urlpatterns = [
    path('', NodesView.as_view(), name='nodes_list'),
    path('storage/', NodesStorageView.as_view(), name='nodes_storage'),
    path('weather-station/', WeatherStationView.as_view(), name='weather_station'),
]
