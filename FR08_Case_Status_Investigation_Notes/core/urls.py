# URL dispatcher for Investigation Case Notes
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('investigation_app.urls')),
]
