"""Handle and manage all the jwt tokens."""
from datetime import (
    datetime,
    timedelta
)
from authlib.jose import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from .utils import make_unique_uuid4_code, read_file


def generate_access_token(email: str) -> str:
    """Generate and return a JWT access token.

    Example: TODO
    -------
    >>> generate_access_token('moseswillfred1@gmail.com')
    >>> "ffer"

    Parameters
    ----------
    email : str
        The email address of the user

    Returns
    -------
    str
        The JWT generated token
    """
    time = datetime.utcnow() + \
        timedelta(minutes=settings.ACCESS_TOKEN_EXP_TIME)

    header = {'alg': 'RS256'}
    access_token_payload = {
        "token_type": "access",
        'email': email,
        'exp': int(time.strftime('%s')),
        'iat': datetime.utcnow(),
        'jti': make_unique_uuid4_code(),
    }
    key = read_file(settings.PRIV_ACCESS_TOKEN_KEY)
    access_token = jwt.encode(
        header, access_token_payload, key).decode('utf-8')

    return access_token


def generate_refresh_token(email: str) -> str:
    """Generate and return a JWT refresh token.

    Parameters
    ----------
    email : str
        The email address of the user

    Returns
    -------
    str
        The generated token
    """
    time = datetime.utcnow() + \
        timedelta(hours=settings.REFRESH_TOKEN_EXP_TIME)

    header = {'alg': 'RS256'}
    refresh_token_payload = {
        "token_type": "refresh",
        'email': email,
        'exp': int(time.strftime('%s')),
        'iat': datetime.utcnow(),
        'jti': make_unique_uuid4_code(),
    }
    key = read_file(settings.PRIV_REFRESH_TOKEN_KEY)
    refresh_token = jwt.encode(
        header, refresh_token_payload, key).decode('utf-8')

    return refresh_token


def generate_password_reset_token():
    """Generate a JWT password reset token"""
    # TODO: Implement password reset token
    raise NotImplementedError('Method not yet implemented.')


def get_token_data(token: str, key: bytes):
    """Check validity of the token and return the payload.

    Parameters
    ----------
    token: str
        The generated user token.

    Returns
    -------
    `User`
        The user.
    """
    from django.contrib.auth import get_user_model  # noqa
    User = get_user_model()
    try:
        payload = jwt.decode(token, key)
        payload.validate()
    except Exception as ex:
        raise AuthenticationFailed(ex)

    try:
        user = User.objects.get(email=payload['email'])
    except User.DoesNotExist:
        msg = 'No user matching this token was found.'
        raise AuthenticationFailed(msg)

    if not user.is_active:
        msg = 'This user has been deactivated.'
        raise AuthenticationFailed(msg)

    return user
