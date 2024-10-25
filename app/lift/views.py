from rest_framework import generics
from rest_framework import parsers
from rest_framework import permissions

from . import models
from . import serializers


class CameraFrameAPIView(generics.CreateAPIView):
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CameraFrameSerializer


class PeopleCountAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CameraPeopleCountSerializer
