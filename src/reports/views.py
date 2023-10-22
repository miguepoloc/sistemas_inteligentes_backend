"""
File for the reports app.
"""

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from reports.models import Visitors
from reports.serializers import VisitorsSerializer


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
        data = request.data
        if request.user.is_authenticated:
            data['user'] = request.user.id
        serializer = VisitorsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Visitor created successfully'}, status=status.HTTP_201_CREATED)
        return Response(
            {'message': 'Visitor not created', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
