from __future__ import annotations

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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


class CameraFrame(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    frame = models.ImageField(upload_to='frames/')
    created_at = models.DateTimeField(auto_now_add=True)


class CameraPeopleCount(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
