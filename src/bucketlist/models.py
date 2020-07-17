"""Models for the bucketlist app."""
from django.contrib.auth import get_user_model
from django.db.models import (
    CharField,
    CASCADE,
    DateTimeField,
    ForeignKey,
    Model,
)

User = get_user_model()


class Bucketlist(Model):
    """Class represents the bucketlist model."""

    name = CharField(
        max_length=255, blank=False, unique=True)
    owner = ForeignKey(
        User, on_delete=CASCADE, related_name='bucketlists')
    date_created = DateTimeField(
        auto_now=False, auto_now_add=True)
    date_modified = DateTimeField(
        auto_now=True, auto_now_add=False)

    def __str__(self):
        """Return a human readable representation of the model."""
        return self.name
