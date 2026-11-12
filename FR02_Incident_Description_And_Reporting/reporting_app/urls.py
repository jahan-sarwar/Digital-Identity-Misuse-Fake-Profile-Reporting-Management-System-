from django.urls import path
from .incident_views import submit_incident_view
from .incident_list_views import incident_list_view
from .incident_detail_views import incident_detail_view

urlpatterns = [
    path('', incident_list_view, name='incident_list'),
    path('submit/', submit_incident_view, name='submit_incident'),
    path('case/<str:case_id>/', incident_detail_view, name='incident_detail'),
]

