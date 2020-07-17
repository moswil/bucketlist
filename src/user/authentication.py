"""Custom authentication backends for the user app."""
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header
)
from rest_framework.exceptions import PermissionDenied

from .helpers.token import get_token_data
from .helpers.utils import read_file


class CSRFCheck(CsrfViewMiddleware):
    """For CSRF checks."""

    def _reject(self, request, reason):
        """Return the failure reason instead of an HttpResponse."""
        return reason


class JWTAuthentication(BaseAuthentication):
    """Called on every request to check if the user is authenticated."""

    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """`authenticate` method is called on every request regardless of whether the endpoint requires authentication.

        `authenticate` has two possible return values:

        1) `None` - We return `None` if we do not wish to authenticate. Usually
                    this means we know authentication will fail. An example of
                    this is when the request does not include a token in the
                    headers.

        2) `(user, token)` - We return a user/token combination when
                             authentication is successful.

                            If neither case is met, that means there's an error
                            and we do not return anything.
                            We simple raise the `AuthenticationFailed`
                            exception and let Django REST Framework
                            handle the rest.
        """
        request.user = None

        # `auth_header` should be an array with two elements: 1) the name of
        # the authentication header (in this case, "Token") and 2) the JWT
        # that we should authenticate against.
        auth_header = get_authorization_header(
            request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Invalid token header. No credentials provided. Do not attempt to
            # authenticate.
            return None

        elif len(auth_header) > 2:
            # Invalid token header. The Token string should not contain spaces. Do
            # not attempt to authenticate.
            return None

        # The JWT library we're using can't handle the `byte` type, which is
        # commonly used by standard libraries in Python 3. To get around this,
        # we simply have to decode `prefix` and `token`. This does not make for
        # clean code, but it is a good decision because we would get an error
        # if we didn't decode these values.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            # The auth header prefix is not what we expected. Do not attempt to
            # authenticate.
            return None

        # By now, we are sure there is a *chance* that authentication will
        # succeed. We delegate the actual credentials authentication to the
        # method below.
        key = read_file(settings.PUB_ACCESS_TOKEN_KEY)
        user = get_token_data(token, key)
        self.ensure_csrf(request)

        return (user, token)

    def ensure_csrf(self, request):
        """Enforce CSRF validation."""
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            # CSRF failed, bail with explicit error message
            raise PermissionDenied(
                'CSRF Failed: %s' % reason)
