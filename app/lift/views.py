from rest_framework import generics
from rest_framework import parsers
from rest_framework import permissions

from . import models
from . import serializers


class ElevatorAPIView(generics.RetrieveAPIView):
    queryset = models.Elevator.objects.all()
    permission_classes = [permissions.AllowAny]  # TODO: Change this to IsAuthenticated
    serializer_class = serializers.ElevatorSerializer
    lookup_url_kwarg = "elevator_id"


class CameraFrameAPIView(generics.CreateAPIView):
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CameraFrameSerializer


class PeopleCountAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CameraPeopleCountSerializer
