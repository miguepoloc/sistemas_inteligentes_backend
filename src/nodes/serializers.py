"""
File with serializers for the nodes app.
"""

from datetime import datetime
from typing import Union

from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from rest_framework import serializers

from nodes.models import Nodes, NodesStorage, WeatherStation
from nodes.utils import excel_to_json


class NodesSerializer(serializers.ModelSerializer):
    """
    A Django REST Framework serializer for the Nodes model.
    """

    class Meta:
        """
        Meta class for the NodesSerializer.
        """

        model = Nodes
        fields = '__all__'


class NodesStorageSerializer(serializers.ModelSerializer):
    """
    A Django REST Framework serializer for the NodesStorage model.
    """

    class Meta:
        """
        Meta class for the NodesStorageSerializer.
        """

        model = NodesStorage
        fields = '__all__'


class DataWeatherStationSerializer(serializers.ModelSerializer):
    """
    A serializer class for the DataWeatherStation model.

    Attributes:
        Meta (class): The Meta class for the DataWeatherStationSerializer.

    Methods:
        create(validated_data: dict) -> [WeatherStation, None]: Creates a new WeatherStation object.
    """

    class Meta:
        """
        Meta class for the WeatherStationSerializer.
        """

        model = WeatherStation
        fields = '__all__'

    def create(self, validated_data: dict) -> Union[WeatherStation, None]:
        """
        Create a new DataWeatherStation object.

        Args:
            validated_data (dict): The validated data from the serializer.

        Returns:
            WeatherStation or None: The created WeatherStation object if it doesn't already exist in the database,
                otherwise None.

        Note:
            - The 'validated_data' should contain the fields required to create a new WeatherStation object.
            - If a WeatherStation object with the same 'date' already exists in the database, None will be returned.
            - Otherwise, a new WeatherStation object will be created using the 'validated_data' and returned.
        """
        if WeatherStation.objects.filter(date=validated_data['date']).exists():
            return None
        return WeatherStation.objects.create(**validated_data)


class WeatherStationSerializer(serializers.Serializer):
    """
    A serializer class for the WeatherStation model.

    Attributes:
        document (FileField): The file field for the document.

    Methods:
        validate_document(value: object) -> object: Validates the 'document' field.
        create(validated_data) -> list: Creates a new WeatherStation object.
    """

    document = serializers.FileField()

    def validate_document(self, value: object) -> object:
        """
        Validates the 'document' field of the WeatherStationSerializer.

        Args:
            value (object): The value of the 'document' field.

        Returns:
            object: The validated 'document' value.

        Raises:
            serializers.ValidationError: If the file is not in .xlsx format.

        Note:
            - The 'document' field should be a FileField.
            - The file must have a .xlsx extension to be considered valid.
        """
        if value.name.endswith('.xlsx'):
            return value
        raise serializers.ValidationError("The file must be in .xlsx format")

    def create(self, validated_data) -> list:
        """
        Create a new WeatherStation object.

        Args:
            validated_data (dict): The validated data from the serializer.

        Returns:
            WeatherStation: The created WeatherStation object.

        Raises:
            serializers.ValidationError: If the data_weather_station_serializer is not valid.

        Note:
            - The 'validated_data' should contain the 'document' field, which is a FileField.
            - The 'document' field should be an Excel file in .xlsx format.
            - The Excel file will be converted to JSON format using the 'excel_to_json' function.
            - The JSON data will be used to create multiple DataWeatherStationSerializer objects.
            - If any of the DataWeatherStationSerializer objects is not valid, a ValidationError will be raised.
            - The valid DataWeatherStationSerializer objects will be saved and returned as a list.
        """
        excel_data = validated_data['document'].read()
        json_data = excel_to_json(excel_data)
        data_weather_station_serializer = DataWeatherStationSerializer(data=json_data, many=True)
        if not data_weather_station_serializer.is_valid():
            raise serializers.ValidationError(data_weather_station_serializer.errors)
        return data_weather_station_serializer.save()


class NodesStorageTxtSerializer(serializers.Serializer):
    """
    Serializer class for handling the storage of nodes data from a .txt file.

    Attributes:
        document (FileField): The file field for the document.
    """

    document = serializers.FileField()

    def validate_document(self, value: UploadedFile) -> UploadedFile:
        """
        Validates the uploaded document file.

        Args:
            value (UploadedFile): The uploaded file object.

        Returns:
            UploadedFile: The validated file object.

        Raises:
            serializers.ValidationError: If the file is not in .txt format.
        """
        if value.name.endswith('.txt'):
            return value
        raise serializers.ValidationError("The file must be in .txt format")

    def create(self, validated_data: dict[str, UploadedFile]) -> list[str]:
        """
        Create method to process and save data from validated_data.

        Args:
            validated_data (dict[str, UploadedFile]): The validated data containing the uploaded file.

        Returns:
            list[str]: A list of responses indicating the success or failure of data creation.

        Raises:
            serializers.ValidationError: If an error occurs during data creation.
        """
        txt_data: bytes = validated_data['document'].read()
        responses: list = []
        for item in str(txt_data).split("\\n"):
            if not item or item.startswith("b'ID_NODO") or item == "'":
                continue
            data: list[str] = item.split(';')
            try:
                defaults: dict[str, str] = {
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
                date_time_naive: datetime = datetime.strptime(data[1], "%Y-%m-%dT%H:%M:%S")
                date_time_aware: datetime = timezone.make_aware(date_time_naive)

                defaults["date_time"] = date_time_aware

                node: Nodes = Nodes.objects.get(id=int(data[0]))  # Get the node instance
                defaults['node'] = node  # Add the node instance to the defaults dictionary

                NodesStorage.objects.get_or_create(node=node, date_time=date_time_aware, defaults=defaults)

                responses.append(f'Node {node.pk} in date {date_time_aware} data created successfully!')
            except Exception as e:
                raise serializers.ValidationError({"error": str(e)})
        return responses
