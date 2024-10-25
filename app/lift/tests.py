from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from . import models


class TestElevator(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test',
            password='test',
        )
        cls.camera = models.Camera.objects.create(
            auth=cls.user,
            name='테스트용 카메라',
            description='테스트용 설명',
        )
        cls.elevator = models.Elevator.objects.create(
            name='테스트용 엘리베이터',
            description='테스트용 설명',
            camera=cls.camera,
        )
        cls.camera_frame = models.CameraFrame.objects.create(
            camera=cls.camera,
            frame=SimpleUploadedFile(
                name='test-camera-frame.png',
                content=open('fixtures/test-camera-image.png', 'rb').read(),
                content_type='image/png',
            ),
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.local_image_file = SimpleUploadedFile(
            name='test-camera-frame.png',
            content=open('fixtures/test-camera-image.png', 'rb').read(),
            content_type='image/png',
        )

    def test_404_카메라가_없는_엘리베이터의_사람_수_데이터_추가(self):
        self.camera.delete()
        res = self.client.post(reverse("cam/count"), data={'count': 10})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_201_카메라가_있는_엘리베이터의_사람_수_데이터_추가(self):
        res = self.client.post(reverse("cam/count"), data={'count': 10})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.CameraPeopleCount.objects.filter(
            camera=self.camera).latest().count, 10)

    def test_404_카메라가_없는_엘리베이터의_사진_데이터_추가(self):
        self.camera.delete()
        res = self.client.post(reverse("cam/frame"), data={'frame': self.local_image_file})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_201_카메라가_있는_엘리베이터의_사진_데이터_추가(self):
        before = models.CameraFrame.objects.filter(camera=self.camera).count()
        res = self.client.post(reverse("cam/frame"), data={'frame': self.local_image_file})
        after = models.CameraFrame.objects.filter(camera=self.camera).count()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.json())
        self.assertEqual(before+1, after)
