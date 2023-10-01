"""
Test custom Django management commands.
"""
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from core.models import Plan, list_of_default_plans

class CommandTests(TestCase):
    """Test commands."""

    def test_create_default_plans(self):
        """Test creating default plans."""

        call_command('create_default_plans')
        default_plans = list_of_default_plans()

        for p in default_plans:
            plan = Plan.objects.get(name=p['name'])
            self.assertEqual(plan.name, p['name'])
