# Module 05: Complainant Identity Verification Submission & Review Handler
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from portal_app.models import IdentityVerification
from portal_app.forms import IdentityVerificationForm
from features.common import log_audit_event, send_case_notification


def handle_verification_submission(request, case):
    # Save complainant ID scan and selfie photograph for officer verification
    form = IdentityVerificationForm(request.POST, request.FILES)
    if form.is_valid():
        ver = form.save(commit=False)
        ver.case = case
        ver.save()
        log_audit_event(
            request, case, 'IDENTITY_SUBMITTED', case.current_status, 'PENDING_VERIFICATION',
            f"Identity verification submitted by {ver.reporter_full_name}."
        )
        messages.success(request, f"Identity documents submitted. Token: {ver.verification_token}")
        return True, form
    return False, form


def handle_verification_decision(request, case):
    # Approve or reject submitted complainant identity verification
    ver_id = request.POST.get('verification_id')
    decision = request.POST.get('decision')
    ver_obj = get_object_or_404(IdentityVerification, id=ver_id, case=case)
    ver_obj.verification_status = 'VERIFIED' if decision == 'APPROVE' else 'REJECTED'
    ver_obj.reviewed_by = request.user.first_name or request.user.username
    ver_obj.reviewed_at = timezone.now()
    ver_obj.save()

    if decision == 'APPROVE' and case.current_status == 'SUBMITTED':
        case.current_status = 'IDENTITY_VERIFIED'
        case.public_status_message = 'Complainant identity verified. Case proceeding to evidence triage.'
        case.save()

    send_case_notification(
        case, case.reporter, case.reporter_email, 'IN_APP',
        f"Identity Verification {ver_obj.verification_status}: {case.case_id}",
        f"Your submitted identity documents have been marked as {ver_obj.get_verification_status_display()}."
    )
    log_audit_event(
        request, case, 'IDENTITY_VERIFIED', 'PENDING', ver_obj.verification_status,
        f"Admin {request.user.username} marked ID verification as {ver_obj.verification_status}."
    )
    messages.success(request, f"Identity verification marked as {ver_obj.verification_status}.")
