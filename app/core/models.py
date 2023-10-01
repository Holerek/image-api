"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class Plan(models.Model):
    name = models.CharField(max_length=255, unique=True)
    thumbnails = models.ManyToManyField('Thumbnail')
    original_size = models.BooleanField()
    expiring_link = models.BooleanField()

    def __str__(self):
        return self.name


class Thumbnail(models.Model):
    size = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f'Thumbnail height: {self.size}px'


class User(AbstractUser):
    plan = models.ForeignKey('Plan', on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)


def list_of_default_plans():
    """Set up list for command create_default_plans"""
    default_plans = [
            {
                'name': 'Basic',
                'thumbnails': [
                    {'size': 200},
                ],
                'original_size': False,
                'expiring_link': False,

            },
            {
                'name': 'Premium',
                'thumbnails': [
                    {'size': 200},
                    {'size': 400},
                ],
                'original_size': True,
                'expiring_link': False,
            },
            {
                'name': 'Enterprise',
                'thumbnails': [
                    {'size': 200},
                    {'size': 400},
                ],
                'original_size': True,
                'expiring_link': True,
            },
        ]
    return default_plans