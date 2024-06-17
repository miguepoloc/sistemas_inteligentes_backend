"""
File for the Nodes views.
"""

# import datetime
# from typing import Union

# from django.core.files.uploadedfile import UploadedFile
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# from core.pagination import CustomPaginationClass
from ripener.models import MachineInfo, NodesInfo
from ripener.serializers import MachineSerializer, NodesSerializer


class MachineView(APIView):
    """
    A Django REST Framework view for the Machine model.

    Attributes:
        permission_classes (tuple): A tuple of permission classes that the view requires.
        serializer_class (NodesSerializer): The serializer class to use for serializing and deserializing data.
    """

    permission_classes = (AllowAny,)
    serializer_class = MachineSerializer

    def get_queryset(self):
        """
        Returns a filtered queryset of active Machine objects.
        """
        if self.request.query_params.get('all'):
            return NodesInfo.objects.all()
        if self.request.query_params.get('machine'):
            return NodesInfo.objects.filter(id=self.request.query_params.get('machine'))
        return NodesInfo.objects.filter(is_active=True)

    def get(self, request) -> Response:
        """
        Handles GET requests and returns a serialized response of all Machine.

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
            return Response(
                {'message': 'machine session created successfully!', 'machine_id': serializer.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'message': 'machine session not created!', "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
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
            machine_info = MachineInfo.objects.get(id=request.data.get('id'))
        except machine_info.DoesNotExist:
            return Response({'message': 'Node not found!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(machine_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': f'Node {machine_info.name} with id {machine_info.id} updated successfully!'},
                status=status.HTTP_200_OK,
            )
        return Response(
            {'message': 'Node not updated!', "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class NodesView(APIView):
    """
    A Django REST Framework view for the Machine model.

    Attributes:
        permission_classes (tuple): A tuple of permission classes that the view requires.
        serializer_class (NodesSerializer): The serializer class to use for serializing and deserializing data.
    """

    permission_classes = (AllowAny,)
    serializer_class = NodesSerializer

    def get_queryset(self):
        """
        Returns a filtered queryset of active Machine objects.
        """
        return MachineInfo.objects.filter(is_active=True)

    def get(self, request) -> Response:
        """
        Handles GET requests and returns a serialized response of all Machine.

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
            machine_info = MachineInfo.objects.get(id=request.data.get('id'))
        except machine_info.DoesNotExist:
            return Response({'message': 'Node not found!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(machine_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': f'Node {machine_info.name} with id {machine_info.id} updated successfully!',
                    'machine_id': serializer.id,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {'message': 'Node not updated!', "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
