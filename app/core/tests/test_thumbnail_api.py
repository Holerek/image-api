"""
Tests for thumbnail APIs.
"""

from core.models import Thumbnail

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.serializers import ThumbnailSerializer

THUMBNAIL_URL = reverse('core:thumbnail-list')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicThumbnailAPITests(TestCase):
    """Test unauthenticated API request"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(THUMBNAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class AdminThumbnailAPITest(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            username='Test User',
            password='testpassword123',
            is_superuser=True,
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_thumbnails(self):
        """Test retrieving a list of thumbnails."""
        Thumbnail.objects.create(size=100)
        Thumbnail.objects.create(size=200)

        res = self.client.get(THUMBNAIL_URL)

        thumbnails = Thumbnail.objects.all().order_by('-id')
        serializer = ThumbnailSerializer(thumbnails, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)