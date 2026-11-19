from django.urls import path
from .signup_views import signup_view
from .login_views import login_view
from .logout_views import logout_view
from .profile_views import profile_view, edit_profile_view
from .admin_views import (
    admin_portal_view,
    approve_user_account,
    reject_user_account,
    accept_case_request,
    reject_case_request,
    submit_case_view
)

# ==============================================================================
# URL Patterns for User Authentication and Administration Portal
# ব্যবহারকারী নিবন্ধন, লগইন এবং অ্যাডমিন অনুমোদন সিস্টেমের পাথ রাউটিং
# ==============================================================================
urlpatterns = [
    # Authentication routes / প্রমাণীকরণ রাউট
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    
    # Victim Case Submission route / ব্যবহারকারীর কেস দাখিল রাউট
    path('submit-case/', submit_case_view, name='submit_case'),

    # Admin Management routes / অ্যাডমিন ব্যবস্থাপনা ও অনুমোদন রাউট
    path('admin-portal/', admin_portal_view, name='admin_portal'),
    path('admin-portal/approve-user/<int:user_id>/', approve_user_account, name='approve_user'),
    path('admin-portal/reject-user/<int:user_id>/', reject_user_account, name='reject_user'),
    path('admin-portal/accept-case/<int:case_id>/', accept_case_request, name='accept_case'),
    path('admin-portal/reject-case/<int:case_id>/', reject_case_request, name='reject_case'),
]
