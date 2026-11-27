from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('governance/approvals/', views.governance_approvals_view, name='governance_approvals'),
]
