# URL patterns for investigation status and notes
from django.urls import path
from . import views

urlpatterns = [
    # Ongoing investigations dashboard
    path('', views.case_journal_list_view, name='case_journal_list'),
    # Case status update & note logging workspace
    path('case/<str:case_id>/', views.update_investigation_view, name='update_investigation'),
]
