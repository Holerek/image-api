"""
Views for the Image APIs.
"""
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.settings import api_settings

from core.models import Thumbnail, Image, User, Plan
from core import serializers


class ThumbnailViewSet(viewsets.ModelViewSet):
    """View for manage Thumbnail API"""
    serializer_class = serializers.ThumbnailSerializer
    queryset = Thumbnail.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    http_method_names = ['get', 'post', 'put', 'delete']


class ImageViewSet(viewsets.ModelViewSet):
    """View for manage Image API"""
    serializer_class = serializers.ImageSerializer
    queryset = Image.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        """Retrieve images for authenticated user."""
        queryset = self.queryset.filter(owner=self.request.user)

        return queryset


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


class ImageList(APIView):
    def _read_thumbnails_size(self, list_of_thumbnails):
        links = {}
        for t in list_of_thumbnails:
            links[f'{t.size}px:'] = 'sample text'
        return links

    def get(self, request, format=None):
        # user = User.objects.get(pk=request.user.id)
        plan = Plan.objects.get(name='Premium')
        plan_ser = serializers.PlanSerializer(plan)
        thumbnails = plan.thumbnails.all()

        thumbnail_links = self._read_thumbnails_size(thumbnails)

        images = Image.objects.all()
        serializer = serializers.ImageListSerializer(images, many=True)

        for image in serializer.data:
            image["original image"] = plan_ser.data['original_size']
            image["expiring link"] = plan_ser.data['expiring_link']
            image.update(thumbnail_links)


        return Response(serializer.data)