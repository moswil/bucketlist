"""Forms for the custom user app."""
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm
)

from .models import User


class UserCreation(UserCreationForm):
    """Custom user creation form."""

    class Meta:
        model = User
        fields = ('email',)


class UserChange(UserChangeForm):
    """Custom user change form."""

    class Meta:
        model = User
        fields = ('email',)
