"""URLs for the user app."""
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    LoginAPIView,
    UserViewSet,
    refresh_token_view
)

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(),
         name='user-login'),
    path('auth/refresh-token/', refresh_token_view,
         name='auth-refresh-token'),
]

urlpatterns += router.urls
