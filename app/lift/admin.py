from django.contrib import admin

from . import models


admin.site.register(models.Elevator)

admin.site.register(models.Camera)

admin.site.register(models.CameraFrame)

admin.site.register(models.PeopleCount)
