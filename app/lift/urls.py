from django.urls import path

from . import views


urlpatterns = [
    path("<uuid:elevator_id>/", views.ElevatorAPIView.as_view(), name="elevator"),
    path("camera/", views.CameraFrameAPIView.as_view(), name="cam/frame"),
    path("people-count/", views.PeopleCountAPIView.as_view(), name="cam/count"),
]
