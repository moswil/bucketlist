"""Serializers for the user app, for registration, login and password reset."""
from django.contrib.auth import authenticate
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
    ValidationError
)

from .helpers.token import generate_access_token
from .models import User


class UserSerializer(ModelSerializer):
    """Serializer class to handle the User model."""

    # access_token = CharField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_staff',
                  'date_joined',)
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        """Create and return a new user."""
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(Serializer):
    """Serializer for logging in users."""

    email = CharField(max_length=255, required=True)
    password = CharField(
        max_length=63, write_only=True, required=True)
    access_token = CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        """Validate email and password against DB records"""
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise ValidationError(
                    msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise ValidationError(msg, code='authorization')

        return {
            'email': user.email,
            'access_token': generate_access_token(user.email),
        }


class PasswordResetSerializer(ModelSerializer):
    """Serializer class to handle password reset via email."""

    email = EmailField(max_length=255, required=True)

    def verify(self, email):
        pass
