# Module 07: Investigator Assignment & Priority Allocation Handler
from django.contrib import messages
from django.utils import timezone
from portal_app.forms import CaseAssignmentForm
from features.common import log_audit_event, send_case_notification


def handle_investigator_assignment(request, case):
    # Assign an approved forensic investigator and set priority SLA
    form = CaseAssignmentForm(request.POST, instance=case)
    if form.is_valid():
        old_status = case.current_status
        obj = form.save(commit=False)
        if obj.assigned_investigator:
            obj.assigned_at = timezone.now()
            if obj.current_status in ['SUBMITTED', 'IDENTITY_VERIFIED', 'EVIDENCE_ACCEPTED']:
                obj.current_status = 'ASSIGNED'
            obj.public_status_message = (
                f"Case assigned to Investigator {obj.assigned_investigator.first_name or obj.assigned_investigator.username}."
            )
        obj.save()
        send_case_notification(
            case, case.reporter, case.reporter_email, 'SMS',
            f"Investigator Assigned: {case.case_id}",
            obj.public_status_message
        )
        log_audit_event(
            request, case, 'ASSIGNED_TO_OFFICER', old_status, obj.current_status,
            f"Assigned to {obj.assigned_investigator.username if obj.assigned_investigator else 'Unassigned'}."
        )
        messages.success(request, "Investigator assigned successfully.")
        return True, form
    return False, form
