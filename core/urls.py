
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf.urls.static import static
from core import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("users.api.urls")),
    path("contactmessage/", include("contactmessages.api.urls")),
    path("files/", include("imagess.api.urls")),
    path("car/", include("cars.api.urls")),
    path("reservations/", include("reservations.api.urls")),
    path("excel/", include("excel.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)