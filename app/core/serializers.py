"""
Serializers for Image APIs.
"""
from django.contrib.auth import authenticate
from rest_framework import serializers

from core.models import Thumbnail, Plan, User, Image


class ThumbnailSerializer(serializers.ModelSerializer):
    """Serializer for thumbnails"""

    class Meta:
        model = Thumbnail
        fields = ['id', 'size']
        read_only_fields = ['id']



class PlanSerializer(serializers.ModelSerializer):
    """Serializer for plans."""
    thumbnails = ThumbnailSerializer(many=True)

    class Meta:
        model = Plan
        fields = ['id', 'name', 'thumbnails', 'original_size', 'expiring_link']
        read_only_fields = ['id']






class UserSerializer(serializers.ModelSerializer):
    """Serializer for thumbnails"""
    plan = PlanSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'plan']
        read_only_fields = ['id']


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )

        if not user:
            msg = ('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class ImageListSerializer(serializers.ModelSerializer):
    """Serializer for uploading images."""

    class Meta:
        model = Image
        fields = ['image']


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images."""

    class Meta:
        model = Image
        fields = ['id', 'image']
        rear_only_fields = ['id']
        extra_kwargs = {
            'image': {'required': 'True'},
        }

    def create(self, validated_data):
        """Create Image"""
        owner = self.context['request'].user
        new_image = Image.objects.create(
            owner = owner,
            **validated_data
        )

        return new_image