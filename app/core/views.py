"""
Views for the Image APIs.
"""
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.settings import api_settings

from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404

from PIL import Image as PILImage
import os
import io

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

    http_method_names = ['post', 'delete']

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
    """View for listing user images and links"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _generate_thumbnail_links(self, list_of_thumbnails, token, image_id):
        links = {}
        for t in list_of_thumbnails:
            host = self.request.get_host()
            url = reverse('core:download', args=[image_id, t.size, token])
            links[f'thumbnail of height {t.size}px:'] = host + url
        return links

    def get(self, request, format=None):
        token = self.request.auth.key
        plan = request.user.plan
        plan_ser = serializers.PlanSerializer(plan)

        images = Image.objects.filter(owner=request.user)
        serializer = serializers.ImageListSerializer(images, many=True)

        thumbnails = plan.thumbnails.all().order_by('size')
        # thumbnail_links = self._read_thumbnails_size(thumbnails, token, images)

        for image in serializer.data:
            image.update(self._generate_thumbnail_links(thumbnails, token, image['id']))

            if plan_ser.data['original_size']:
                image['original image'] = self.request.get_host() + image['image']

            if plan_ser.data['expiring_link']:
                image['expiring link'] = 'TO DO'

            image['image'] = os.path.basename(image['image'])
        return Response(serializer.data)


def thumbnailView(request, image_id, size, token):
    image = get_object_or_404(Image, pk=image_id)
    user = get_object_or_404(Token, key=token).user
    allowed_thumbnails = [t.size for t in user.plan.thumbnails.all()]

    if image.owner == user and size in allowed_thumbnails:
        with PILImage.open(image.image.path) as original_image:
            # calculate new width
            aspect_ration = original_image.width / original_image.height
            new_width = int(size * aspect_ration)

            # prepare new buffer
            buffer = io.BytesIO()

            # convert and resize image
            thumbnail = original_image.resize((new_width, size), PILImage.ANTIALIAS)
            thumbnail.convert('RGB').save(buffer, 'JPEG')

            # create and set up a response
            response = HttpResponse(buffer.getvalue(), content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="thumbnail-{image_id}-height-{size}px.jpg"'

            return response
    return HttpResponse(f'error: {status.HTTP_401_UNAUTHORIZED} unauthorized')