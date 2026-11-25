# Views for Security Audit Trail and History Log
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import SecurityAuditTrail
import csv

def populate_seed_audits():
    # Helper to generate seed audit events if empty
    if not SecurityAuditTrail.objects.exists():
        SecurityAuditTrail.objects.create(
            case_id='CASE-2026-5501',
            action_category='CASE_SUBMITTED',
            actor_username='citizen.sarwar',
            actor_role='Complainant',
            ip_address='103.205.71.12',
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0',
            previous_state='None',
            new_state='SUBMITTED',
            action_narrative='Incident complaint registered alleging Facebook identity impersonation and extortion.'
        )
        SecurityAuditTrail.objects.create(
            case_id='CASE-2026-5501',
            action_category='IDENTITY_VERIFIED',
            actor_username='officer.sarwar',
            actor_role='Triage Officer',
            ip_address='192.168.1.45',
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/121.0',
            previous_state='PENDING',
            new_state='VERIFIED',
            action_narrative='Complainant National ID credentials inspected and cross-verified against official directory.'
        )
        SecurityAuditTrail.objects.create(
            case_id='CASE-2026-5501',
            action_category='ASSIGNED_TO_OFFICER',
            actor_username='admin.controller',
            actor_role='Supervisory Desk',
            ip_address='192.168.1.10',
            user_agent='SecurityConsole/4.1 (Linux; x86_64)',
            previous_state='UNASSIGNED',
            new_state='ASSIGNED_TO_SARWAR',
            action_narrative='Case allocated to Lead Forensic Detective Sarwar Jahan (Badge CID-CYBER-014).'
        )
        SecurityAuditTrail.objects.create(
            case_id='CASE-2026-5501',
            action_category='PLATFORM_TAKEDOWN_ISSUED',
            actor_username='detective.sarwar',
            actor_role='Lead Detective',
            ip_address='192.168.1.45',
            user_agent='SecurityConsole/4.1 (Linux; x86_64)',
            previous_state='IN_PROGRESS',
            new_state='TAKEDOWN_ISSUED',
            action_narrative='Emergency takedown notice transmitted to Meta Trust Operations under reference FB-LEGAL-77291.'
        )


def audit_dashboard_view(request):
    # Ensure seed records exist
    populate_seed_audits()

    audit_logs = SecurityAuditTrail.objects.all()

    # Filter parameters
    case_query = request.GET.get('case_id', '').strip()
    category_filter = request.GET.get('category', '').strip()

    if case_query:
        audit_logs = audit_logs.filter(case_id__icontains=case_query)
    if category_filter:
        audit_logs = audit_logs.filter(action_category=category_filter)

    # Export to CSV feature
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Case_Audit_Security_Trail.csv"'
        writer = csv.writer(response)
        writer.writerow(['Timestamp', 'Case ID', 'Action Category', 'Actor', 'Role', 'IP Address', 'Narrative', 'SHA-256 Hash'])
        for a in audit_logs:
            writer.writerow([a.timestamp, a.case_id, a.get_action_category_display(), a.actor_username, a.actor_role, a.ip_address, a.action_narrative, a.event_hash])
        return response

    # Metrics
    total_logs = SecurityAuditTrail.objects.count()
    unique_cases = SecurityAuditTrail.objects.values('case_id').distinct().count()
    verified_hashes = SecurityAuditTrail.objects.filter(is_tamper_verified=True).count()

    context = {
        'audit_logs': audit_logs,
        'total_logs': total_logs,
        'unique_cases': unique_cases,
        'verified_hashes': verified_hashes,
        'case_query': case_query,
        'selected_category': category_filter or 'ALL',
    }
    return render(request, 'audit_app/audit_dashboard.html', context)


def case_audit_detail_view(request, case_id):
    # Show audit history for a single specific case
    logs = SecurityAuditTrail.objects.filter(case_id=case_id).order_by('timestamp')
    return render(request, 'audit_app/case_audit_detail.html', {
        'case_id': case_id,
        'logs': logs,
    })
