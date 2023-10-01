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
        Returns a filtered queryset of Nodes objects.
        """
        return Nodes.objects.filter(is_active=True)

    def get(self, request):
        """
        GET method for the NodesView.
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        POST method for the NodesView.
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
        PUT method for the NodesView.
        """
        try:
            node = Nodes.objects.get(id=request.data.get('id'))
        except Nodes.DoesNotExist:
            return Response({'message': 'Node not found!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(node, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Node updated successfully!'}, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Node not updated!', "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class NodesStorageView(APIView):
    """
    A Django REST Framework view for the NodesStorage model.
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
        GET method for the NodesStorageView.
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        POST method for the NodesStorageView.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Node data created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(
            {'message': 'Node data not created!', "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request):
        """
        PUT method for the NodesStorageView.
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Node data updated successfully!'}, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Node data not updated!', "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
