"""
Views for the Image APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from core.models import Thumbnail
from core import serializers


class ThumbnailViewSet(viewsets.ModelViewSet):
    """View for manage Thumbnail API"""
    serializer_class = serializers.ThumbnailSerializer
    queryset = Thumbnail.objects.all().order_by('-id')
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
