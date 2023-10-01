"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from core.models import Plan, Thumbnail


def create_user(username='Test Username', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_successful(self):
        """Test creating a user is successful"""
        username = 'Test Username'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))


    def test_new_user_without_username_raises_error(self):
        """Test that crating a user without an username raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')


    def test_create_superuser(self):
        """Test crating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_create_thumbnail_with_positive_size(self):
        """Test creating a thumbnail"""
        size = 200
        thumbnail = Thumbnail.objects.create(size=size,)

        self.assertEqual(thumbnail.size, size)


    def test_create_thumbnail_with_negative_size(self):
        """Test creating a thumbnail that should fail"""
        size = -200
        with self.assertRaises(IntegrityError):
            thumbnail = Thumbnail.objects.create(size=size)


    def test_create_plan(self):
        """Test creating a plan"""
        name = 'Sample plan name'
        original_size = True
        expiring_link = False

        plan = Plan.objects.create(
            name=name,
            original_size = original_size,
            expiring_link = expiring_link,
        )

        self.assertEqual(plan.name, name)
        self.assertTrue(plan.original_size)
        self.assertFalse(plan.expiring_link)
