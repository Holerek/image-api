"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from django.test import TestCase

from core.models import Plan, Thumbnail, list_of_default_plans

class CommandTests(TestCase):
    """Test commands."""

    def test_create_default_plans(self):
        """Test creating default plans."""

        call_command('create_default_plans')
        default_plans = list_of_default_plans()

        for p in default_plans:
            thumbnails = p.pop('thumbnails')
            plan = Plan.objects.get(name=p['name'])

            self.assertEqual(plan.name, p['name'])
            self.assertEqual(plan.original_size, p['original_size'])
            self.assertEqual(plan.expiring_link, p['expiring_link'])

    @patch('core.management.commands.wait_for_db.Command.check')
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('core.management.commands.wait_for_db.Command.check')
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
