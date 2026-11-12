from django.shortcuts import render
from .models import IncidentReport

def incident_list_view(request):
    """
    FR-02: Dedicated Case List View.
    Displays all submitted complaints and their tracking statuses.
    """
    incidents = IncidentReport.objects.all()
    return render(request, 'reporting_app/incident_list.html', {
        'incidents': incidents,
        'title': 'Track Incident Reports - FR-02'
    })

