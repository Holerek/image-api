"""
Serializers for Image APIs.
"""
from rest_framework import serializers

from core.models import Thumbnail, Plan


class ThumbnailSerializer(serializers.ModelSerializer):
    """Serializer for thumbnails"""

    class Meta:
        model = Thumbnail
        fields = ['id', 'size']
        read_only_fields = ['id']