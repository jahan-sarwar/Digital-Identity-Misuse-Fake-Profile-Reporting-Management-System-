# URL patterns for Administrative Portal and User Management
from django.urls import path
from . import views

urlpatterns = [
    # Executive dashboard
    path('', views.admin_dashboard_overview_view, name='admin_dashboard'),
    # Administrative User Approval Queue
    path('admin/approvals/', views.user_approval_queue_view, name='user_approval_queue'),
    path('approvals/', views.user_approval_queue_view),
    # Public sign-up
    path('auth/signup/', views.user_signup_view, name='user_signup'),
    # System login & logout
    path('auth/login/', views.user_login_view, name='user_login'),
    path('auth/logout/', views.user_logout_view, name='user_logout'),
]
