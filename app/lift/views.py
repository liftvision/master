from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import parsers
from rest_framework import permissions

from . import models
from . import serializers


class CameraFrameAPIView(generics.CreateAPIView, generics.RetrieveAPIView):
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CameraFrameSerializer

    def get_object(self):
        return get_object_or_404(models.Camera, auth=self.request.user).get_latest_frame_or_404()


class PeopleCountAPIView(generics.CreateAPIView, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CameraPeopleCountSerializer

    def get_object(self):
        return get_object_or_404(models.Camera, auth=self.request.user).get_latest_people_count_or_404()
