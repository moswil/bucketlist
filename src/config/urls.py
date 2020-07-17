"""config URL Configuration."""
from django.contrib import admin
from django.urls import include, path

from bucketlist.urls import urlpatterns as bucketlist_urls
from user.urls import urlpatterns as user_urls

api_urls = bucketlist_urls + user_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urls)),
]
