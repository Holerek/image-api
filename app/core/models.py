"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Plan(models.Model):
    name = models.CharField(max_length=255, unique=True)


def list_of_default_plans():
    default_plans = [
            {
                'name': 'Basic',
            },
            {
                'name': 'Premium',
            },
            {
                'name': 'Enterprise',
            },
        ]
    return default_plans