# URL patterns for the unified SafeIdentity Official Platform
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('report/new/', views.submit_report_view, name='submit_report'),
    path('cases/', views.case_list_view, name='case_list'),
    path('cases/<str:case_id>/', views.case_detail_view, name='case_detail'),
    path('track/', views.public_tracker_view, name='public_tracker'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/read/<int:notif_id>/', views.mark_notification_read_view, name='mark_notification_read'),
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),
    path('governance/approvals/', views.governance_approvals_view, name='governance_approvals'),
]
