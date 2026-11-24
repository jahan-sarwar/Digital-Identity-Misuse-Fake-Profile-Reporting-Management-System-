# URL patterns for identity verification routing
from django.urls import path
from . import views

urlpatterns = [
    # Citizen identity verification submission page
    path('', views.submit_verification_view, name='submit_verification'),
    # Individual status tracking page by token
    path('status/<uuid:token>/', views.verification_status_view, name='verification_status'),
    # Official document verification review portal
    path('portal/review/', views.verification_review_portal_view, name='verification_review_portal'),
]
