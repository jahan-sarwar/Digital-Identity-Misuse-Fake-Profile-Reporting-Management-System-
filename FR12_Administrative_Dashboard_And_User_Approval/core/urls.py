# URL dispatcher for Administrative Operations
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('dashboard_app.urls')),
    path('admin/', admin.site.urls),
]
