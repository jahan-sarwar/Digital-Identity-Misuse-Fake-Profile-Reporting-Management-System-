# URL routing for Investigator Assignment Portal
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('assignment_app.urls')),
]
