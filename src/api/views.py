import time

from django.conf import settings
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import DateLogSerializer, DateReadingsSerializer

SUCCESS_RESPONSE = {"response": "Successfully resgistered"}


def data_dict_to_points(data: dict):
    readings = data["readings"]

    points = (
        Point("weather")
        .tag("location", "Tijuana")
        .field("temperature", reading["temperature"])
        for reading in readings
    )
    return points


def save_to_influxdb(data):
    point_series = (data_dict_to_points(date) for date in data)

    with InfluxDBClient(
        url=settings.INFLUX_URL, org=settings.INFLUX_ORG, token=settings.INFLUX_TOKEN
    ) as client:
        with client.write_api(write_options=ASYNCHRONOUS) as write_api:
            for series in point_series:
                for point in series:
                    write_api.write(settings.INFLUX_BUCKET, settings.INFLUX_ORG, point)
                    time.sleep(1)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def multiple_dates_temperature(request):
    serializer = DateReadingsSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        save_to_influxdb(serializer.validated_data)
        data = SUCCESS_RESPONSE
    else:
        data = serializer.errors
    return Response(data)


# Original implementation, no longer in use
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def temperature_readings(request):
    serializer = DateLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = SUCCESS_RESPONSE
    else:
        data = serializer.errors
    return Response(data)
