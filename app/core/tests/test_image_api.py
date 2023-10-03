"""
Tests for thumbnail APIs.
"""
import tempfile
import os
from io import BytesIO

from PIL import Image as PILImage

from core.models import Image, Plan, Thumbnail, list_of_default_plans

from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


IMAGE_URL = reverse('core:image-list')
LIST_URL = reverse('core:list')
ME_URL = reverse('core:me')
TOKEN_URL = reverse('core:token')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicAPITests(TestCase):
    """Test unauthenticated API request"""

    def setUp(self):
        self.client = APIClient()

    def test_image_auth_required(self):
        """Test auth is required to call image-list API"""
        res = self.client.post(IMAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_image_auth_required(self):
        """Test uploading an image required auth"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = PILImage.new('RGB', (100, 100))
            img.save(image_file, format='JPEG')
            # go back to begging of the file
            image_file.seek(0)
            payload = {
                'image': image_file,
            }
            res = self.client.post(IMAGE_URL, payload, format='multipart')

            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserAPITest(TestCase):
    """Test for regular authenticated users"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            username='Test User',
            password='testpassword123',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)

        # create and save test image
        img = PILImage.new('RGB', (1600, 1000))
        img_io = BytesIO()
        img.save(img_io, format='JPEG')

        image_file = File(img_io)
        self.image = Image(owner=self.user)
        self.image.image.save('test.jpg', image_file)
        self.image.save()

        # create default plans
        default_plans = list_of_default_plans()
        for plan in default_plans:
            thumbnails = plan.pop('thumbnails')
            p, created = Plan.objects.get_or_create(name=plan['name'], defaults=plan)

            for thumbnail in thumbnails:
                t, _ = Thumbnail.objects.get_or_create(size=thumbnail['size'])
                p.thumbnails.add(t)

            p.save()

    def tearDown(self):
        self.image.image.delete()

    def test_check_user_view(self):
        """Test user auth correctly"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], self.user.username)

    def test_upload_image(self):
        """Test uploading an image"""
        file_name = 'test-upload-file'
        with tempfile.NamedTemporaryFile(prefix=file_name, suffix='.jpg') as image_file:
            img = PILImage.new('RGB', (100, 100))
            img.save(image_file, format='JPEG')
            # go back to begging of the file
            image_file.seek(0)
            payload = {
                'image': image_file,
            }
            res = self.client.post(IMAGE_URL, payload, format='multipart')

            image_from_db = Image.objects.get(image__contains=file_name)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            self.assertIn('image', res.data)
            self.assertTrue(os.path.exists(image_from_db.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image."""
        payload = {'image': 'notanimage'}
        res = self.client.post(IMAGE_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_basic_plan_user(self):
        """Test basic plan access"""

        self.user.plan = Plan.objects.get(name='Basic')
        thumbnails = self.user.plan.thumbnails.values()

        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for t in thumbnails:
            self.assertIn(f'thumbnail of height {t["size"]}px:', res.data[0])
        self.assertNotIn('original image', res.data[0])
        self.assertNotIn('expiring link', res.data[0])

    def test_premium_plan_user(self):
        """Test basic plan access"""

        self.user.plan = Plan.objects.get(name='Premium')
        thumbnails = self.user.plan.thumbnails.values()

        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for t in thumbnails:
            self.assertIn(f'thumbnail of height {t["size"]}px:', res.data[0])
        self.assertIn('original image', res.data[0])
        self.assertNotIn('expiring link', res.data[0])

    def test_enterprise_plan_user(self):
        """Test basic plan access"""

        self.user.plan = Plan.objects.get(name='Enterprise')
        thumbnails = self.user.plan.thumbnails.values()

        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for t in thumbnails:
            self.assertIn(f'thumbnail of height {t["size"]}px:', res.data[0])
        self.assertIn('original image', res.data[0])
        self.assertIn('expiring link', res.data[0])
