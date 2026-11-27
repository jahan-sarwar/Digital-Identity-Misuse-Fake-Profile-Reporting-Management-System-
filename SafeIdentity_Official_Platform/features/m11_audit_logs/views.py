# Module 11: Security Audit History Log & CSV Export
import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from portal_app.models import SecurityAuditTrail


@login_required
def audit_logs_view(request):
    # Display SHA-256 tamper-evident audit logs and handle CSV export
    if request.user.profile.role not in ['ADMIN', 'INVESTIGATOR']:
        messages.error(request, "Authorization required to view security audit trails.")
        return redirect('dashboard')

    logs = SecurityAuditTrail.objects.all()
    case_q = request.GET.get('case_id', '').strip()
    if case_q:
        logs = logs.filter(case_ref__icontains=case_q)

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="SafeIdentity_Audit_Trail.csv"'
        writer = csv.writer(response)
        writer.writerow(['Timestamp', 'Case Ref', 'Category', 'Actor', 'Role', 'IP Address', 'Narrative', 'SHA-256 Digest'])
        for entry in logs:
            writer.writerow([entry.timestamp, entry.case_ref, entry.action_category, entry.actor_username, entry.actor_role, entry.ip_address, entry.action_narrative, entry.event_hash])
        return response

    return render(request, 'portal_app/audit_logs.html', {
        'logs': logs,
        'case_q': case_q,
    })
