"""The models for the user app."""
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone


from user.helpers.token import (
    generate_access_token,
)

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    email = models.EmailField(
        ("email address"), max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """Return a human readable representation of the model."""
        return self.email

    @property
    def access_token(self):
        """Return a generated JWT token."""
        return generate_access_token(self.email)
