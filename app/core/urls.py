"""
URL mappings for the core app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from core import views


router = DefaultRouter()

router.register('thumbnails', views.ThumbnailViewSet)
router.register('images', views.ImageViewSet)
# router.register('list', views.ImageList)

app_name = 'core'
urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.CheckUserView.as_view(), name='me'),
    path('list/', views.ImageList.as_view(), name='list'),
]