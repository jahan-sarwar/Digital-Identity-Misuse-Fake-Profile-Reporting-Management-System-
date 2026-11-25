# URL routing for Security Audit System
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('audit_app.urls')),
]
