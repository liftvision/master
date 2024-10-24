from __future__ import annotations

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from rest_framework import exceptions


class Elevator(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    camera = models.ForeignKey('Camera', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    camera: models.ForeignKey[Camera]

    def __str__(self):
        return self.name

    def update_people_count(self, count: int):
        self.get_camera_or_404().update_people_count(count)

    def update_camera_frame(self, frame):
        self.get_camera_or_404().update_frame(frame)

    def get_camera_or_404(self) -> Camera:
        if self.camera is None:
            raise exceptions.NotFound('Elevator does not have a camera associated.')
        return self.camera

    def get_latest_camera_frame_or_404(self) -> CameraFrame:
        return self.get_camera_or_404().get_latest_frame_or_404()

    def get_latest_camera_people_count_or_404(self) -> CameraPeopleCount:
        return self.get_camera_or_404().get_latest_people_count_or_404()


class Camera(models.Model):
    @staticmethod
    def on_delete(collector, field, sub_objs, using):
        collector.add_field_update("auth", None, sub_objs)
        collector.add_field_update("deleted", True, sub_objs)
        collector.add_field_update("deleted_at", timezone.now(), sub_objs)

    auth = models.ForeignKey(User, on_delete=on_delete.__func__, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def update_frame(self, frame):
        CameraFrame.objects.create(camera=self, frame=frame)

    def update_people_count(self, count: int):
        CameraPeopleCount.objects.create(camera=self, count=count)

    def get_latest_frame_or_404(self) -> CameraFrame:
        try:
            return CameraFrame.objects.filter(camera=self).latest()
        except CameraFrame.DoesNotExist:
            raise exceptions.NotFound('Camera does not have any frame recorded.')

    def get_latest_people_count_or_404(self) -> CameraPeopleCount:
        try:
            return CameraPeopleCount.objects.filter(camera=self).latest()
        except CameraPeopleCount.DoesNotExist:
            raise exceptions.NotFound('Camera does not have any people count recorded.')


class CameraFrame(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    frame = models.ImageField(upload_to='frames/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'


class CameraPeopleCount(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'
