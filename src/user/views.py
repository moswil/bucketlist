"""Views for the user app."""
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import (
    csrf_protect,
    ensure_csrf_cookie,
)

from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import (
    CreateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import (
    ModelViewSet,
)

from .helpers.token import (
    generate_access_token,
    generate_refresh_token,
    get_token_data
)
from .helpers.utils import read_file
from .models import User
from .serializers import (
    LoginSerializer,
    UserSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def refresh_token_view(request):
    """Obtain a new access_token.

    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    """
    refresh_token = request.COOKIES.get('refreshtoken')
    print(f'REF: {refresh_token}')
    if refresh_token is None:
        msg = 'Authentication credentials were not provided.'
        raise AuthenticationFailed(
            msg, code='authentication')
    key = read_file(settings.PUB_REFRESH_TOKEN_KEY)
    user = get_token_data(refresh_token, key)
    access_token = generate_access_token(user.email)
    return Response({'access_token': access_token}, HTTP_200_OK)


class UserViewSet(ModelViewSet):
    """Creates a user."""

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """Instantiate and returns the list of permissions that this view requires."""
        if self.action == 'create':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]


class LoginAPIView(CreateAPIView):
    """Checks the email and password, and returns auth token."""

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        """Handle user login."""
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        refresh_token = generate_refresh_token(
            user.get('email'))
        response = Response()
        response.set_cookie(
            key='refreshtoken', value=refresh_token, httponly=True)
        response.data = serializer.data
        return response
