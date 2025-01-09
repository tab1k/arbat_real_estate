from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('website.urls')),
    path('users/', include('users.urls')),
    path('managers/', include('managers.urls')),
    path('realtors/', include('realtors.urls')),
    path('applications/', include('applications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)