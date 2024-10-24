from django.contrib import admin
from django.utils.html import format_html
from rest_framework import exceptions

from . import models


@admin.register(models.Elevator)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'uuid',
        'camera',
        'get_frame',
        'get_people_count',
    ]
    search_fields = [
        'name',
        'description',
    ]
    list_filter = [
        'created_at',
        'updated_at',
    ]

    @admin.display(description='frame')
    def get_frame(self, obj: models.Elevator):
        try:
            return format_html(f'<img src="{obj.get_camera_or_404().get_latest_frame_or_404().frame.url}" height="64" />')
        except exceptions.NotFound:
            return None

    @admin.display(description='people count')
    def get_people_count(self, obj: models.Elevator):
        try:
            return obj.get_camera_or_404().get_latest_people_count_or_404().count
        except exceptions.NotFound:
            return None


@admin.register(models.Camera)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_associated_user',
        'get_frame',
        'updated_at',
    ]
    search_fields = [
        'name',
    ]
    list_filter = [
        'updated_at',
    ]

    @admin.display(description='associated user')
    def get_associated_user(self, obj: models.Camera):
        if obj.auth is None:
            return None
        return obj.auth.username

    @admin.display(description='frame')
    def get_frame(self, obj: models.Camera):
        try:
            return format_html(f'<img src="{obj.get_latest_frame_or_404().frame.url}" height="64" />')
        except exceptions.NotFound:
            return None


@admin.register(models.CameraFrame)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        'camera',
        'get_frame',
        'created_at',
    ]
    search_fields = [
        'camera__name',
        'created_at',
    ]
    list_filter = [
        'created_at',
    ]

    @admin.display(description='frame')
    def get_frame(self, obj: models.CameraFrame):
        return format_html(f'<img src="{obj.frame.url}" height="64" />')


@admin.register(models.CameraPeopleCount)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        'camera',
        'count',
        'created_at',
    ]
    search_fields = [
        'camera__name',
        'created_at',
    ]
    list_filter = [
        'created_at',
    ]
