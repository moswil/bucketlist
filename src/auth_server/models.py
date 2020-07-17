"""Models for the auth server app."""
from django.db.models import (
    CharField,
    Model,
    ForeignKey,
    CASCADE,
    TextField
)
from django.contrib.auth import get_user_model
from authlib.oauth2.rfc6749 import ClientMixin

User = get_user_model()


class OAuth2Client(Model, ClientMixin):
    """Client making protected resource requests on behalf of resource owner."""

    user = ForeignKey(User, on_delete=CASCADE)
    client_id = CharField(
        max_length=48, unique=True, db_index=True)
    client_secret = CharField(max_length=48, blank=True)
    client_name = CharField(max_length=120)
    redirect_uris = TextField(default='')
    default_redirect_uri = TextField(
        blank=False, default='')
    scope = TextField(default='')
    response_type = TextField(default='')
    grant_type = TextField(default='')
    token_endpoint_auth_method = CharField(
        max_length=120, default='')

    def get_client_id(self) -> str:
        """Return the unique identifier for the client, `client_id`."""
        return self.client_id

    def get_default_redirect_uri(self):
        """Return the client default redirect uri."""
        return self.default_redirect_uri
