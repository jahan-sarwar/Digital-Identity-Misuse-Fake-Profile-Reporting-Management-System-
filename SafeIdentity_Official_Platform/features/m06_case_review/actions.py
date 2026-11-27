# Module 06: Administrative Case & Evidence Triage Review Handler
from django.contrib import messages
from django.utils import timezone
from portal_app.forms import CaseTriageReviewForm
from features.common import log_audit_event


def handle_case_triage(request, case):
    # Save risk assessment and evidence triage verdict
    form = CaseTriageReviewForm(request.POST, instance=case)
    if form.is_valid():
        old_status = case.current_status
        obj = form.save(commit=False)
        obj.reviewed_by = request.user.first_name or request.user.username
        obj.reviewed_at = timezone.now()
        obj.save()
        log_audit_event(
            request, case, 'CASE_TRIAGED', old_status, obj.current_status,
            f"Risk assessed as {obj.risk_level}; status set to {obj.current_status}."
        )
        messages.success(request, "Administrative triage assessment saved.")
        return True, form
    return False, form
