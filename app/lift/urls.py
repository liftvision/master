from django.urls import path

from . import views


urlpatterns = [
    path("camera/", views.CameraFrameAPIView.as_view(), name="cam/frame"),
    path("people-count/", views.PeopleCountAPIView.as_view(), name="cam/count"),
]
