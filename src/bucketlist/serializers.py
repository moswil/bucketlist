"""Serializers for the bucketlist app."""
from rest_framework.serializers import (
    ReadOnlyField,
    ModelSerializer,
)

from .models import Bucketlist


class BucketlistSerializer(ModelSerializer):
    """Serializer to map the model instance to JSON format."""

    owner = ReadOnlyField(source='owner.email')

    class Meta:
        """Meta class to map the serializer's fields with the model fields."""

        model = Bucketlist
        fields = ('id', 'name', 'owner', 'date_created',
                  'date_modified',)
        read_only_fields = (
            'date_created', 'date_modified',)
