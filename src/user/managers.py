"""Custom managers for the user app models."""
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifier.

    In the builtin user model, username is used for authentication. This
    custom manager enables us to use email instead.
    """

    def create_user(self, email, password, **kwargs):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(
                'Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """Create and save a superuser with the given email and password."""
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff set to True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser set to True')
        return self.create_user(email, password, **kwargs)
