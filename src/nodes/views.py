"""
File for the Nodes views.
"""

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from nodes.models import Nodes, NodesStorage
from nodes.serializers import NodesSerializer, NodesStorageSerializer


class NodesView(APIView):
    """
    A Django REST Framework view for the Nodes model.
    """

    permission_classes = (AllowAny,)
    serializer_class = NodesSerializer

    def get_queryset(self):
        """
        Returns a filtered queryset of active Nodes objects.
        """
        return Nodes.objects.filter(is_active=True)

    def get(self, request):
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

    def post(self, request):
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
    """

    permission_classes = (AllowAny,)
    serializer_class = NodesStorageSerializer

    def get_queryset(self):
        """
        Returns a filtered queryset of NodesStorage objects.
        """
        return NodesStorage.objects.filter(is_active=True)

    def get(self, request):
        """
        Handles GET requests. Retrieves the queryset, serializes the data, and returns the response.

        Parameters:
        - request: The GET request object.

        Returns:
        - Response: The serialized data response.
        """
        queryset = self.get_queryset().order_by("-created_at")
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
