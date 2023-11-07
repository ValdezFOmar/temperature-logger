from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import DateLogSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def temperature_readings(request):
    serializer = DateLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {"response": "Successfully resgistered"}
    else:
        data = serializer.errors
    return Response(data)
