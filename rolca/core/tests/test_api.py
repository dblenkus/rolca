# pylint: disable=missing-docstring
from datetime import date, timedelta
from mock import MagicMock, Mock, patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from rolca.core.api.viewsets import PhotoViewSet, SalonViewSet
from rolca.core.models import Author, File, Photo, Salon, Theme


class SalonApiTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.salon_list_view = SalonViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
        self.salon_detail_view = SalonViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })

        self.user = MagicMock(spec=get_user_model(), is_superuser=False)
        self.super_user = MagicMock(spec=get_user_model(), is_superuser=True)

    @patch('rolca.core.api.viewsets.SalonViewSet.create')
    def test_create_permissions(self, salon_create_mock):
        salon_create_mock.return_value = MagicMock(spec=Response)
        request = self.factory.post('', {}, format='json')

        # public user
        resp = self.salon_list_view(request)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_create_mock.call_count, 0)

        # normal user
        force_authenticate(request, self.user)
        resp = self.salon_list_view(request)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_create_mock.call_count, 0)

        # admin user
        force_authenticate(request, self.super_user)
        resp = self.salon_list_view(request)
        self.assertEqual(salon_create_mock.call_count, 1)

    @patch('rolca.core.api.viewsets.SalonViewSet.list')
    def test_get_list_permissions(self, salon_list_mock):
        salon_list_mock.return_value = MagicMock(spec=Response)
        request = self.factory.get('', format='json')

        # public user
        self.salon_list_view(request)
        self.assertEqual(salon_list_mock.call_count, 1)
        salon_list_mock.reset_mock()

        salon_list_mock.reset_mock()

        # normal user
        force_authenticate(request, self.user)
        self.salon_list_view(request)
        self.assertEqual(salon_list_mock.call_count, 1)

    @patch('rolca.core.api.viewsets.SalonViewSet.retrieve')
    def test_get_detail_permissions(self, salon_retrieve_mock):
        salon_retrieve_mock.return_value = MagicMock(spec=Response)
        request = self.factory.get('', format='json')

        # public user
        self.salon_detail_view(request, pk=1)
        self.assertEqual(salon_retrieve_mock.call_count, 1)

        salon_retrieve_mock.reset_mock()

        # normal user
        force_authenticate(request, self.user)
        self.salon_detail_view(request, pk=1)
        self.assertEqual(salon_retrieve_mock.call_count, 1)

    @patch('rolca.core.api.viewsets.SalonViewSet.update')
    def test_put_permissions(self, salon_update_mock):
        salon_update_mock.return_value = MagicMock(spec=Response)
        request = self.factory.put('', {}, format='json')

        # public user
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_update_mock.call_count, 0)

        # normal user
        force_authenticate(request, self.user)
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_update_mock.call_count, 0)

        # admin user
        force_authenticate(request, self.super_user)
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(salon_update_mock.call_count, 1)

    @patch('rolca.core.api.viewsets.SalonViewSet.partial_update')
    def test_patch_permissions(self, salon_update_mock):
        salon_update_mock.return_value = MagicMock(spec=Response)
        request = self.factory.patch('', {}, format='json')

        # public user
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_update_mock.call_count, 0)

        # normal user
        force_authenticate(request, self.user)
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_update_mock.call_count, 0)

        # admin user
        force_authenticate(request, self.super_user)
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(salon_update_mock.call_count, 1)

    @patch('rolca.core.api.viewsets.SalonViewSet.destroy')
    def test_delete_permissions(self, salon_destroy_mock):
        salon_destroy_mock.return_value = MagicMock(spec=Response)
        request = self.factory.delete('', {}, format='json')

        # public user
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_destroy_mock.call_count, 0)

        # normal user
        force_authenticate(request, self.user)
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_destroy_mock.call_count, 0)

        # admin user
        force_authenticate(request, self.super_user)
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(salon_destroy_mock.call_count, 1)


class PhotoViewSetTest(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user1 = user_model.objects.create_user(username='user1')
        self.user2 = user_model.objects.create_user(username='user2')
        self.judge = user_model.objects.create_user(username='judge')

        today = date.today()
        self.salon = Salon.objects.create(
            owner=self.judge,
            title='Test salon',
            start_date=today,
            end_date=today,
            jury_date=today + timedelta(days=1),
            results_date=today + timedelta(days=2))
        self.salon.judges.add(self.judge)

        theme = Theme.objects.create(title='Test theme', salon=self.salon, n_photos=2)

        author1 = Author.objects.create(uploader=self.user1)
        author2 = Author.objects.create(uploader=self.user2)

        file_mock = SimpleUploadedFile('photo.jpg', b'fake photo')

        # pk must be set to skip on-create procedure
        self.file1 = File.objects.create(pk=1, user=self.user1, file=file_mock)
        self.file2 = File.objects.create(pk=2, user=self.user2, file=file_mock)
        self.file3 = File.objects.create(pk=3, user=self.user2, file=file_mock)

        Photo.objects.create(
            title="Photo 1", user=self.user1, author=author1, theme=theme, photo=self.file1)
        Photo.objects.create(
            title="Photo 2", user=self.user2, author=author2, theme=theme, photo=self.file2)
        Photo.objects.create(
            title="Photo 3", user=self.user2, author=author2, theme=theme, photo=self.file3)

    def tearDown(self):
        self.file1.file.delete()
        self.file2.file.delete()
        self.file3.file.delete()

    def test_photo_queryset(self):
        viewset_mock = Mock(spec=PhotoViewSet)

        viewset_mock.request = Mock(user=self.user2)
        self.assertEqual(len(PhotoViewSet.get_queryset(viewset_mock)), 2)

        viewset_mock.request = Mock(user=self.judge)
        self.assertEqual(len(PhotoViewSet.get_queryset(viewset_mock)), 3)

        self.salon.results_date = date.today() - timedelta(days=1)
        self.salon.save()

        viewset_mock.request = Mock(user=self.user2)
        self.assertEqual(len(PhotoViewSet.get_queryset(viewset_mock)), 3)
