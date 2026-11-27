# Root URL dispatcher connecting all modular feature packages into one unified website
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from features.m12_admin_governance.views import governance_approvals_view


def admin_redirect(request):
    return redirect('/login/?role=admin')


urlpatterns = [
    # Safe redirect for legacy /admin/ URLs so users never get trapped in default dark Django login
    path('admin/approvals/', governance_approvals_view, name='legacy_admin_approvals'),
    path('admin/login/', admin_redirect, name='admin_login_redirect'),
    path('admin/', admin_redirect, name='admin_root_redirect'),

    # Standard Django admin under custom path
    path('django-admin/', admin.site.urls),

    # Feature Modules
    path('', include('features.m01_user_auth.urls')),
    path('', include('features.m02_incident_reporting.urls')),
    path('', include('features.m08_investigation_notes.urls')),
    path('', include('features.m09_public_tracker.urls')),
    path('', include('features.m10_notifications.urls')),
    path('', include('features.m11_audit_logs.urls')),
    path('', include('features.m12_admin_governance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
