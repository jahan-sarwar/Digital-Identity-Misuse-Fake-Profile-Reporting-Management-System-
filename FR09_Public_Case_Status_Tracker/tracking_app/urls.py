# URL routing for Citizen Case Tracking
from django.urls import path
from . import views

urlpatterns = [
    # Citizen public tracking homepage
    path('', views.public_case_tracker_view, name='public_case_tracker'),
]
