"""Views for the bucketlist app."""
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.viewsets import ModelViewSet

from .models import Bucketlist
from .permissions import IsOwner
from .serializers import BucketlistSerializer


class BucketlistViewSet(ModelViewSet):
    """Defines the HTTP methods for CRUD of a bucketlist."""

    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_class = (IsAuthenticated, IsOwner,)

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save(owner=self.request.user)
