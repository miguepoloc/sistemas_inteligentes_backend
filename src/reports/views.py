"""
File for the reports app.
"""

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from reports.models import Visitors
from reports.serializers import VisitorsSerializer
from user.models import User


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
        page = request.data.get('page')
        if not page:
            return Response({'message': 'Page is required'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            data['user'] = request.user.id
        data['ip_address'] = request.META.get('REMOTE_ADDR')
        data['page'] = page

        serializer = VisitorsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Visitor created successfully'}, status=status.HTTP_201_CREATED)
        return Response(
            {'message': 'Visitor not created', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        """
        Handles GET requests and returns the visitors.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A response containing all the visitors.
        """
        visitors = Visitors.objects.all()
        pages = visitors.values('page').distinct()
        visitors_distinct = visitors.distinct('ip_address')
        users = User.objects.all()
        citys = users.values('city').distinct()
        data = [
            {
                "category": "Visitas",
                "count": visitors.count(),
                "data": [],
            },
            {
                "category": "Visitantes",
                "count": visitors_distinct.count(),
                "data": [],
            },
            {
                "category": "Usuarios",
                "count": users.count(),
                "data": [],
            },
        ]

        for page in pages:
            data[0]['data'].append(
                {
                    "name": page['page'],
                    "value": visitors.filter(page=page['page']).count(),
                }
            )
            data[1]['data'].append(
                {
                    "name": page['page'],
                    "value": visitors_distinct.filter(page=page['page']).count(),
                }
            )
        for city in citys:
            data[2]['data'].append(
                {
                    "name": city['city'],
                    "value": users.filter(city=city['city']).count(),
                }
            )
        for item in data:
            item['data'] = sorted(item['data'], key=lambda x: x['value'], reverse=True)
        return Response(data=data, status=status.HTTP_200_OK)
