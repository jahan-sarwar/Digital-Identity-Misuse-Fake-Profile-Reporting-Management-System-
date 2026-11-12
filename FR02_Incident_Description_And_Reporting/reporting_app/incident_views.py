from django.shortcuts import render, redirect
from django.contrib import messages
from .incident_forms import IncidentSubmissionForm

def submit_incident_view(request):
    """
    FR-02: Dedicated Incident Report Submission View.
    Validates narrative description, issues tracking Case ID, and saves to database.
    """
    if request.method == 'POST':
        form = IncidentSubmissionForm(request.POST)
        if form.is_valid():
            incident = form.save()
            messages.success(request, f"Incident successfully filed! Assigned Tracking Case ID: {incident.case_id}")
            return redirect('incident_detail', case_id=incident.case_id)
        else:
            messages.error(request, "Failed to submit incident report. Please correct the errors below.")
    else:
        form = IncidentSubmissionForm()

    return render(request, 'reporting_app/submit_incident.html', {
        'form': form,
        'title': 'File Incident Report - FR-02'
    })

