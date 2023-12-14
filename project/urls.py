from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('portifolio.urls')),
    path('webchat/', include('webchat.urls')),
    path('admin/', admin.site.urls),
]
