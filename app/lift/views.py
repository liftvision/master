from django.views.decorators import gzip
from django.http import HttpRequest
from django.http import StreamingHttpResponse
from rest_framework import generics
from rest_framework import parsers
from rest_framework import permissions

from . import models
from . import serializers


class ElevatorAPIView(generics.RetrieveAPIView):
    queryset = models.Elevator.objects.all()
    permission_classes = [permissions.AllowAny]  # TODO: Change this to IsAuthenticated
    serializer_class = serializers.ElevatorSerializer
    lookup_url_kwarg = "elevator_id"


class ElevatorLiveStreamingView(generics.GenericAPIView):
    queryset = models.Elevator.objects.all()
    permission_classes = [permissions.AllowAny]  # TODO: Change this to IsAuthenticated
    serializer_class = None
    lookup_url_kwarg = "elevator_id"

    @classmethod
    def as_view(cls, **initkwargs):
        return gzip.gzip_page(super().as_view(**initkwargs))

    def get(self, request: HttpRequest, *args, **kwargs):
        return StreamingHttpResponse(self._get_streamer(self.get_object()), content_type='multipart/x-mixed-replace; boundary=frame')

    def _get_streamer(self, object: models.Elevator):
        while True:
            frame = object.get_latest_camera_frame_or_404().frame.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n'
                   b'\r\n'
                   + frame +
                   b'\r\n')


class CameraFrameAPIView(generics.CreateAPIView):
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CameraFrameSerializer


class PeopleCountAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CameraPeopleCountSerializer
