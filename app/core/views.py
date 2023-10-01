"""
Views for the Image APIs.
"""
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.settings import api_settings

from core.models import Thumbnail
from core import serializers


class ThumbnailViewSet(viewsets.ModelViewSet):
    """View for manage Thumbnail API"""
    serializer_class = serializers.ThumbnailSerializer
    queryset = Thumbnail.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    http_method_names = ['get', 'post', 'put', 'delete']


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CheckUserView(RetrieveAPIView):
    """Manage the authenticated user."""
    serializer_class = serializers.UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
