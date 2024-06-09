"""
File for the Nodes views.
"""

from django.core.files.uploadedfile import UploadedFile
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.pagination import CustomPaginationClass
from nodes.models import Nodes, NodesStorage, WeatherStation
from nodes.serializers import (
    DataWeatherStationSerializer,
    NodesSerializer,
    NodesStorageSerializer,
    NodesStorageTxtSerializer,
    WeatherStationSerializer,
)


class NodesView(APIView):
    """
    A Django REST Framework view for the Nodes model.

    Attributes:
        permission_classes (tuple): A tuple of permission classes that the view requires.
        serializer_class (NodesSerializer): The serializer class to use for serializing and deserializing data.
    """

    permission_classes = (AllowAny,)
    serializer_class = NodesSerializer

    def get_queryset(self):
        """
        Returns a filtered queryset of active Nodes objects.
        """
        return Nodes.objects.filter(is_active=True)

    def get(self, request) -> Response:
        """
        Handles GET requests and returns a serialized response of all nodes.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A serialized response of all nodes.
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request) -> Response:
        """
        Handles POST requests and creates a new node if the data is valid.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A response indicating whether the node was created successfully or not.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Node created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(
            {'message': 'Node not created!', "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request):
        """
        Handles PUT requests and updates an existing node if the data is valid.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A response indicating whether the node was updated successfully or not.
        """
        try:
            node = Nodes.objects.get(id=request.data.get('id'))
        except Nodes.DoesNotExist:
            return Response({'message': 'Node not found!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(node, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': f'Node {node.name} with id {node.id} updated successfully!'}, status=status.HTTP_200_OK
            )
        return Response(
            {'message': 'Node not updated!', "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class NodesStorageView(APIView):
    """
    A Django REST Framework view for handling GET and POST requests for the NodesStorage model.

    Attributes:
        permission_classes (tuple): A tuple of permission classes that the view requires.
        serializer_class (NodesStorageSerializer): The serializer class to use for serializing and deserializing data.
        pagination_class (CustomPaginationClass): The pagination class to use for paginating the data.
    """

    permission_classes = (AllowAny,)
    serializer_class = NodesStorageSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        """
        Returns a filtered queryset of NodesStorage objects.
        """
        return NodesStorage.objects.filter(is_active=True)

    def get(self, request) -> Response:
        """
        Handles GET requests. Retrieves the queryset, serializes the data, and returns the response.

        Parameters:
        - request: The GET request object.

        Returns:
        - Response: The serialized data response.
        """
        queryset = self.get_queryset().order_by("-created_at")
        paginator = self.pagination_class()

        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Handles POST requests. Extracts the data from the request, validates it, saves it, and returns the response.

        Parameters:
        - request: The POST request object.

        Returns:
        - Response: The success or error message response.
        """
        request_data = request.body.decode('utf-8').split('\n') if request.body else None
        if not request_data:
            return Response({'message': 'Please provide data!'}, status=status.HTTP_400_BAD_REQUEST)

        responses = []
        for item in request_data:
            data = item.split(';')
            try:
                data_storage = {
                    'node': data[0],
                    "date_time": data[1],
                    "temperature": data[2],
                    "humidity": data[3],
                    "pressure": data[4],
                    "altitude": data[5],
                    "humidity_hd38": data[6],
                    "humidity_soil": data[7],
                    "temperature_soil": data[8],
                    "conductivity_soil": data[9],
                    "ph_soil": data[10],
                    "nitrogen_soil": data[11],
                    "phosphorus_soil": data[12],
                    "potassium_soil": data[13],
                    "battery_level": data[14],
                }
            except IndexError:
                return Response({'message': 'Format data is not correct!'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=data_storage)
            if serializer.is_valid():
                serializer.save()
                responses.append(f'Node {data_storage["node"]} data created successfully!')
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'messages': responses}, status=status.HTTP_201_CREATED)


class NodesStorageTxtView(APIView):
    """
    A view for storing text documents in the system.

    This view handles the HTTP POST request for uploading a text document to the system.
    The document is expected to be provided as a file in the request data.

    Attributes:
        None

    Methods:
        post(request): Handles the HTTP POST request for uploading a text document.
    """

    def post(self, request) -> Response:
        """
        Handles the HTTP POST request for uploading a text document.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """
        document: UploadedFile = request.data.get('document')
        if not document:
            return Response({'message': 'Please provide a document!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = NodesStorageTxtSerializer(data={'document': document})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Document uploaded successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeatherStationView(APIView):
    """
    A Django REST Framework view for the Nodes model.

    Attributes:
        permission_classes (tuple): A tuple of permission classes that the view requires.
        serializer_class (NodesSerializer): The serializer class to use for serializing and deserializing data.
    """

    permission_classes = (AllowAny,)
    pagination_class = CustomPaginationClass
    get_queryset = WeatherStation.objects.all()

    def post(self, request) -> Response:
        """
        Handles POST requests and uploads a document.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A response indicating whether the document was uploaded successfully or not.
        """
        document = request.data.get('document')
        serializer = WeatherStationSerializer(data={'document': document})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Document uploaded successfully"}, status=status.HTTP_201_CREATED)

        return Response(
            {"error": "Error uploading document", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request) -> Response:
        """
        Handles GET requests and returns a serialized response of all documents.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A serialized response of all documents.
        """
        paginator = self.pagination_class()

        page = paginator.paginate_queryset(self.get_queryset, request)

        if page is not None:
            serializer = DataWeatherStationSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.serializer_class(self.get_queryset, many=True)
        return Response(serializer.data)
