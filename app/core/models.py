"""
Database models.
"""
import os
import uuid

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager


def image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    # ext = os.path.splitext(filename)[1]
    # filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'images', filename)


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


class UserManager(AbstractUserManager):
    """Manager for users."""

    def create_user(self, username, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not username:
            raise ValueError('User must have a username.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, **extra_fields):
        """Create and return a new superuser"""
        user = self.create_user(username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    plan = models.ForeignKey('Plan', on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)

    objects = UserManager()


class Image(models.Model):
    image = models.ImageField(upload_to=image_file_path)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')


@receiver(pre_delete, sender=Image)
def delete_image(sender, instance, **kwargs):
    # Delete an image
    instance.image.delete(False)


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
