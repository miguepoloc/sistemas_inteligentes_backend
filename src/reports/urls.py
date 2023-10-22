"""
File that contains the urls of the reports app.
"""

from django.urls import path

from reports.views import VisitorsView

APP_NAME = 'reports'

urlpatterns = [
    path('visitor/', VisitorsView.as_view(), name='visitor'),
]
