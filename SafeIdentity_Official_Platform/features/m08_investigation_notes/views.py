# Module 08: Case Detail Hub, Status Updates & Forensic Investigation Journal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from portal_app.models import IncidentCase, InvestigationNoteEntry
from portal_app.forms import (
    EvidenceUploadForm, IdentityVerificationForm, CaseTriageReviewForm,
    CaseAssignmentForm, InvestigationProgressForm, InvestigationNoteForm
)
from features.common import log_audit_event, send_case_notification
from features.m04_evidence_upload.actions import handle_evidence_upload
from features.m05_identity_verification.actions import handle_verification_submission, handle_verification_decision
from features.m06_case_review.actions import handle_case_triage
from features.m07_investigator_assign.actions import handle_investigator_assignment


@login_required
def case_detail_view(request, case_id):
    # Unified case workspace delegating each action to its dedicated feature module
    case = get_object_or_404(IncidentCase.objects.select_related('assigned_investigator'), case_id=case_id)
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'CITIZEN'
    is_staff_role = user_role in ['ADMIN', 'INVESTIGATOR']

    # Security Gate: Citizens can only view their own registered cases
    if user_role == 'CITIZEN':
        if case.reporter != request.user and case.reporter_email != request.user.email:
            messages.error(request, "Access Denied: You do not have permission to view this case.")
            return redirect('dashboard')

    evidences = case.evidences.all()
    verifications = case.verifications.all()
    notes = case.notes.all()

    if not is_staff_role:
        notes = notes.filter(is_confidential=False)

    evidence_form = EvidenceUploadForm()
    verify_form = IdentityVerificationForm(initial={'reporter_full_name': case.reporter_name})
    triage_form = CaseTriageReviewForm(instance=case)
    assign_form = CaseAssignmentForm(instance=case)
    progress_form = InvestigationProgressForm(instance=case)
    note_form = InvestigationNoteForm()

    if request.method == 'POST':
        action = request.POST.get('action_type')

        if action == 'UPLOAD_EVIDENCE':
            ok, evidence_form = handle_evidence_upload(request, case)
            if ok:
                return redirect('case_detail', case_id=case.case_id)

        elif action == 'SUBMIT_VERIFICATION':
            ok, verify_form = handle_verification_submission(request, case)
            if ok:
                return redirect('case_detail', case_id=case.case_id)

        elif action == 'VERIFY_DECISION' and user_role == 'ADMIN':
            handle_verification_decision(request, case)
            return redirect('case_detail', case_id=case.case_id)

        elif action == 'SAVE_TRIAGE' and user_role == 'ADMIN':
            ok, triage_form = handle_case_triage(request, case)
            if ok:
                return redirect('case_detail', case_id=case.case_id)

        elif action == 'ASSIGN_INVESTIGATOR' and user_role == 'ADMIN':
            ok, assign_form = handle_investigator_assignment(request, case)
            if ok:
                return redirect('case_detail', case_id=case.case_id)

        elif action == 'UPDATE_INVESTIGATION' and is_staff_role:
            old_status = case.current_status
            progress_form = InvestigationProgressForm(request.POST, instance=case)
            if progress_form.is_valid():
                obj = progress_form.save()
                if old_status != obj.current_status:
                    InvestigationNoteEntry.objects.create(
                        case=case,
                        officer_name=request.user.first_name or request.user.username,
                        note_type='STATUS_CHANGE',
                        previous_status=old_status,
                        new_status=obj.current_status,
                        detailed_notes=f"Milestone transitioned from {old_status} to {obj.current_status}."
                    )
                    send_case_notification(
                        case, case.reporter, case.reporter_email, 'EMAIL',
                        f"Case Update [{case.case_id}]: {obj.get_current_status_display()}",
                        obj.public_status_message
                    )
                log_audit_event(
                    request, case, 'STATUS_TRANSITION', old_status, obj.current_status,
                    f"Investigation status updated to {obj.current_status}."
                )
                messages.success(request, "Investigation progress updated.")
                return redirect('case_detail', case_id=case.case_id)

        elif action == 'ADD_NOTE' and is_staff_role:
            note_form = InvestigationNoteForm(request.POST)
            if note_form.is_valid():
                n = note_form.save(commit=False)
                n.case = case
                n.officer_name = request.user.first_name or request.user.username
                n.save()
                log_audit_event(
                    request, case, 'NOTE_LOGGED', case.current_status, case.current_status,
                    f"Added {n.get_note_type_display()} note."
                )
                messages.success(request, "Forensic note added to case journal.")
                return redirect('case_detail', case_id=case.case_id)

    return render(request, 'portal_app/case_detail.html', {
        'case': case,
        'evidences': evidences,
        'verifications': verifications,
        'notes': notes,
        'evidence_form': evidence_form,
        'verify_form': verify_form,
        'triage_form': triage_form,
        'assign_form': assign_form,
        'progress_form': progress_form,
        'note_form': note_form,
        'user_role': user_role,
        'is_staff_role': is_staff_role,
    })
