# URL patterns for case review system
from django.urls import path
from . import views

urlpatterns = [
    # Review queue overview
    path('', views.case_review_list_view, name='case_review_list'),
    # Detailed case triage and evidence review page
    path('case/<str:case_id>/', views.case_detail_review_view, name='case_detail_review'),
]
