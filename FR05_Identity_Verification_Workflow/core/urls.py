# URL routing configuration
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin administration portal
    path('admin/', admin.site.urls),
    # Verification application routing
    path('', include('verification_app.urls')),
]

# Serve uploaded media during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
