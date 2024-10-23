from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import Serializer

from . import models


class CameraFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CameraFrame
        fields = ["frame"]

    def create(self, validated_data):
        validated_data["camera"] = get_camera_or_404(self)
        return super().create(validated_data)


class CameraPeopleCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CameraPeopleCount
        fields = ["count"]

    def create(self, validated_data):
        validated_data["camera"] = get_camera_or_404(self)
        return super().create(validated_data)


def get_camera_or_404(serializer: Serializer):
    user = serializers.CurrentUserDefault()(serializer)
    return get_object_or_404(models.Camera, auth=user)
