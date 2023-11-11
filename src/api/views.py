from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import DateLogSerializer, DateReadingsSerializer

SUCCESS_RESPONSE = {"response": "Successfully resgistered"}


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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def multiple_dates_temperature(request):
    serializer = DateReadingsSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        data = SUCCESS_RESPONSE
    else:
        data = serializer.errors
    return Response(data)
