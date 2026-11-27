# Module 04: Supporting Evidence Upload & Validation Handler
from django.contrib import messages
from portal_app.forms import EvidenceUploadForm
from features.common import log_audit_event


def handle_evidence_upload(request, case):
    # Validate and store uploaded screenshot or PDF evidence for a case
    form = EvidenceUploadForm(request.POST, request.FILES)
    if form.is_valid():
        ev = form.save(commit=False)
        ev.case = case
        ev.uploaded_by = request.user if request.user.is_authenticated else None
        ev.save()
        log_audit_event(
            request, case, 'EVIDENCE_UPLOADED', case.current_status, case.current_status,
            f"Uploaded evidence file ({ev.get_file_type_display()})."
        )
        messages.success(request, "Supporting evidence uploaded and validated.")
        return True, form
    return False, form
