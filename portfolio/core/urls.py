from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include('apps.home.urls')),
    path('webchat/', include('apps.webchat.urls')),
    path('picpay/', include('apps.picpay.urls')),
    path('igreja/', include('apps.igreja.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
