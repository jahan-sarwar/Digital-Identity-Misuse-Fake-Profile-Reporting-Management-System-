# Module 02: Incident Description, Reporting & Case Directory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from portal_app.models import IncidentCase, UserProfile
from portal_app.forms import IncidentSubmissionForm, EvidenceUploadForm
from portal_app.seed import ensure_seed_data
from features.common import log_audit_event, send_case_notification


@login_required
def home_view(request):
    # Main entry point: redirect authenticated users straight to their dashboard
    return redirect('dashboard')


@login_required
def submit_report_view(request):
    # Submit incident report with description, platform URL, and optional initial evidence
    ensure_seed_data()
    initial = {
        'reporter_name': request.user.first_name or request.user.username,
        'reporter_email': request.user.email,
    }

    if request.method == 'POST':
        form = IncidentSubmissionForm(request.POST)
        evidence_form = EvidenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            case_obj = form.save(commit=False)
            case_obj.reporter = request.user
            case_obj.save()

            if request.FILES.get('file') and evidence_form.is_valid():
                ev = evidence_form.save(commit=False)
                ev.case = case_obj
                ev.uploaded_by = request.user
                ev.save()

            send_case_notification(
                case_obj, case_obj.reporter, case_obj.reporter_email, 'EMAIL',
                f"Complaint Registered: {case_obj.case_id}",
                f"Your fake-profile report '{case_obj.title}' has been registered. Case ID: {case_obj.case_id}, Security PIN: {case_obj.security_pin}."
            )
            log_audit_event(
                request, case_obj, 'CASE_SUBMITTED', 'None', 'SUBMITTED',
                f"Submitted report '{case_obj.title}' targeting {case_obj.get_platform_display()}."
            )
            messages.success(
                request,
                f"Report submitted! Case ID: {case_obj.case_id} | Tracking PIN: {case_obj.security_pin}."
            )
            return redirect('case_detail', case_id=case_obj.case_id)
    else:
        form = IncidentSubmissionForm(initial=initial)
        evidence_form = EvidenceUploadForm()

    return render(request, 'portal_app/submit_report.html', {
        'form': form,
        'evidence_form': evidence_form,
    })


@login_required
def case_list_view(request):
    # Filterable incident case directory (Citizens see only their own cases; Staff see all)
    ensure_seed_data()
    cases = IncidentCase.objects.select_related('assigned_investigator').all()

    if request.user.profile.role == 'CITIZEN':
        cases = cases.filter(Q(reporter=request.user) | Q(reporter_email=request.user.email))
    elif request.user.profile.role == 'INVESTIGATOR':
        cases = cases.filter(assigned_investigator=request.user)

    q = request.GET.get('q', '').strip()
    status_f = request.GET.get('status', '').strip()
    risk_f = request.GET.get('risk', '').strip()

    if q:
        cases = cases.filter(Q(case_id__icontains=q) | Q(title__icontains=q) | Q(reporter_name__icontains=q))
    if status_f:
        cases = cases.filter(current_status=status_f)
    if risk_f:
        cases = cases.filter(risk_level=risk_f)

    return render(request, 'portal_app/case_list.html', {
        'cases': cases,
        'q': q,
        'status_f': status_f,
        'risk_f': risk_f,
    })
