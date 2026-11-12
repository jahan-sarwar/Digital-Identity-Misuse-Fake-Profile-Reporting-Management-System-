from django.urls import path
from .submission_views import submit_platform_url_view
from .tracking_views import platform_list_view, platform_case_detail_view

urlpatterns = [
    path('', platform_list_view, name='platform_list'),
    path('submit/', submit_platform_url_view, name='submit_platform_url'),
    path('case/<str:case_id>/', platform_case_detail_view, name='platform_case_detail'),
]

