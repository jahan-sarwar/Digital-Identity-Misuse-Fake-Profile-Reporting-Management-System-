from django.shortcuts import render, get_object_or_404
from .models import IncidentReport

def incident_detail_view(request, case_id):
    """
    FR-02: Dedicated Incident Narrative Detail View.
    Renders the complete narrative description, timeline, and current case status.
    """
    incident = get_object_or_404(IncidentReport, case_id=case_id)
    return render(request, 'reporting_app/incident_detail.html', {
        'incident': incident,
        'title': f"Case {incident.case_id} - FR-02"
    })

