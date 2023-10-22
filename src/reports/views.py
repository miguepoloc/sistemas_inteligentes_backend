"""
File for the reports app.
"""

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from reports.serializers import VisitorsSerializer
from reports.utils import get_ip_info


class VisitorsView(APIView):
    """
    A Django REST Framework view for the Visitors model.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handles POST requests and creates a new visitor if the data is valid.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A response indicating whether the visitor was created successfully or not.
        """
        data = {}
        if request.user.is_authenticated:
            data['user'] = request.user.id
        ip_info = get_ip_info(request.META.get('REMOTE_ADDR'))
        data['ip_address'] = ip_info.ip
        try:
            data['latitude'] = ip_info.latitude
            data['longitude'] = ip_info.longitude
            data['city'] = ip_info.city
            data['region'] = ip_info.region
            data['country'] = ip_info.country_name
        except AttributeError:
            pass
        serializer = VisitorsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Visitor created successfully'}, status=status.HTTP_201_CREATED)
        return Response(
            {'message': 'Visitor not created', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
