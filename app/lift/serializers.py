from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import Serializer

from . import models


class CameraFrameSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source="frame.url", read_only=True)

    class Meta:
        model = models.CameraFrame
        fields = [
            "url",
            "frame",
            "created_at",
        ]
        extra_kwargs = {
            "frame": {"write_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data["camera"] = get_camera_or_404(self)
        return super().create(validated_data)


class CameraPeopleCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CameraPeopleCount
        fields = [
            "count",
            "created_at",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data["camera"] = get_camera_or_404(self)
        return super().create(validated_data)


def get_camera_or_404(serializer: Serializer):
    user = serializers.CurrentUserDefault()(serializer)
    return get_object_or_404(models.Camera, auth=user)


class CameraSerializer(serializers.ModelSerializer):
    frame = CameraFrameSerializer(source="get_latest_frame")
    people_count = CameraPeopleCountSerializer(
        source="get_latest_people_count")

    class Meta:
        model = models.Camera
        fields = [
            "name",
            "description",
            "frame",
            "people_count",
        ]


class ElevatorSerializer(serializers.ModelSerializer):
    camera = CameraSerializer()

    class Meta:
        model = models.Elevator
        fields = [
            "name",
            "description",
            "camera",
        ]
