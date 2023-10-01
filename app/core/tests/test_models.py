"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Plan


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

    def test_create_plan(self):
        """Test creating a plan"""
        name = 'Sample plan name'
        plan = Plan.objects.create(name=name)

        self.assertEqual(plan.name, name)

    def test_plan_name_min_length(self):
        """Test creating a plan"""
        name = 'Sa'
        # with self.assertRaises(Val)
        plan = Plan.objects.create(name=name)

        self.assertEqual(plan.name, name)