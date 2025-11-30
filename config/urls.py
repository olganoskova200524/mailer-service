from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mailing.views import IndexView
from users.views import UserLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("", include("mailing.urls")),
    path("accounts/login/", UserLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
