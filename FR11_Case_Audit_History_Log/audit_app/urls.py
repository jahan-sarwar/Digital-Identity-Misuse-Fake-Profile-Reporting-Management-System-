# URL patterns for audit history system
from django.urls import path
from . import views

urlpatterns = [
    # Global security audit dashboard
    path('', views.audit_dashboard_view, name='audit_dashboard'),
    # Specific case audit timeline
    path('case/<str:case_id>/', views.case_audit_detail_view, name='case_audit_detail'),
]
