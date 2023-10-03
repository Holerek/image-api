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

IMAGE_URL = reverse('core:image-list')
LIST_URL = reverse('core:list')
ME_URL = reverse('core:me')

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

    def test_image_list_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserAPITest(TestCase):
    """Test for regular authenticated users"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            username='Test User',
            password='testpassword123',
        )
        self.client.force_authenticate(self.user)

    def test_check_user_view(self):
        """Test user auth correctly"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], self.user.username)