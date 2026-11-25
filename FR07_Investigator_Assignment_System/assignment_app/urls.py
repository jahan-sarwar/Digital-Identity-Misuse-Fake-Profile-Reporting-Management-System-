# URL endpoints for investigator assignment
from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard showing roster and case assignments
    path('', views.assignment_dashboard_view, name='assignment_dashboard'),
    # Specific case assignment execution page
    path('assign/<str:case_id>/', views.assign_case_view, name='assign_case'),
]
