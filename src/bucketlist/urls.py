"""URLs for the bucketlist app."""
from rest_framework.routers import SimpleRouter

from .views import BucketlistViewSet

bucketlist_router = SimpleRouter()
bucketlist_router.register(
    'bucketlist', BucketlistViewSet, basename='bucket')

urlpatterns = bucketlist_router.urls
