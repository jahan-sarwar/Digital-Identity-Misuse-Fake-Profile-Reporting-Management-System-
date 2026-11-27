# Unified views implementing all reporting, verification, investigation, tracking, notification, audit, and governance workflows
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q

from .models import (
    UserProfile, IncidentCase, EvidenceFile, IdentityVerification,
    InvestigationNoteEntry, CaseEventNotification, SecurityAuditTrail
)
from .forms import (
    RegistrationForm, LoginForm, ProfileUpdateForm, IncidentSubmissionForm,
    EvidenceUploadForm, IdentityVerificationForm, CaseTriageReviewForm,
    CaseAssignmentForm, InvestigationProgressForm, InvestigationNoteForm
)
from .seed import ensure_seed_data


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def log_audit_event(request, case_obj, category, prev_state, new_state, narrative):
    # Helper to append a SHA-256 tamper-evident audit entry
    actor = request.user.username if request.user.is_authenticated else 'anonymous'
    role = request.user.profile.get_role_display() if request.user.is_authenticated and hasattr(request.user, 'profile') else 'Citizen'
    SecurityAuditTrail.objects.create(
        case=case_obj,
        case_ref=case_obj.case_id if case_obj else 'SYSTEM',
        action_category=category,
        actor_username=actor,
        actor_role=role,
        ip_address=get_client_ip(request),
        previous_state=prev_state,
        new_state=new_state,
        action_narrative=narrative
    )


def send_case_notification(case_obj, recipient_user, email, channel, subject, body):
    # Helper to dispatch an in-app/email/SMS notification record
    CaseEventNotification.objects.create(
        case=case_obj,
        recipient=recipient_user,
        recipient_email=email,
        channel=channel,
        subject=subject,
        message_body=body
    )


def home_view(request):
    # Public landing portal with quick case tracker and platform overview
    ensure_seed_data()
    sample_cases = IncidentCase.objects.all()[:3]
    stats = {
        'total_cases': IncidentCase.objects.count(),
        'resolved_cases': IncidentCase.objects.filter(current_status='RESOLVED').count(),
        'active_investigators': UserProfile.objects.filter(role='INVESTIGATOR', is_approved=True).count(),
    }
    return render(request, 'portal_app/home.html', {
        'sample_cases': sample_cases,
        'stats': stats,
    })


def register_view(request):
    # User sign-up workflow requiring subsequent administrative approval
    ensure_seed_data()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['full_name']
            )
            profile = user.profile
            profile.role = form.cleaned_data['requested_role']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.is_approved = False
            profile.approval_status = 'PENDING_APPROVAL'
            profile.save()

            log_audit_event(
                request, None, 'USER_REGISTERED', 'None', 'PENDING_APPROVAL',
                f"New account '{user.username}' registered requesting role {profile.role}."
            )
            messages.success(
                request,
                f"Registration submitted for '{user.username}'. Your account is pending Administrative Approval before login is permitted."
            )
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'portal_app/register.html', {'form': form})


def login_view(request):
    # Login authentication enforcing administrative approval gatekeeper
    ensure_seed_data()
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']

            # Allow login by username or email
            matched_user = User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()
            if matched_user:
                user = authenticate(request, username=matched_user.username, password=password)
                if user is not None:
                    if not user.profile.is_approved:
                        messages.error(
                            request,
                            f"ACCESS DENIED: Account '{user.username}' is currently {user.profile.get_approval_status_display()}. Please wait for Security Administrator approval."
                        )
                    else:
                        login(request, user)
                        log_audit_event(
                            request, None, 'USER_LOGIN', 'LOGGED_OUT', 'AUTHENTICATED',
                            f"User '{user.username}' signed in."
                        )
                        messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                        return redirect('dashboard')
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'portal_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been securely logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    # Account profile management
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name', request.user.first_name)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save()
            form.save()
            messages.success(request, "Account profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'email': request.user.email,
        })
    return render(request, 'portal_app/profile.html', {'form': form, 'profile': profile})


@login_required
def dashboard_view(request):
    # Role-aware executive and operational dashboard
    ensure_seed_data()
    role = request.user.profile.role

    if role == 'CITIZEN':
        cases = IncidentCase.objects.filter(
            Q(reporter=request.user) | Q(reporter_email=request.user.email)
        )
    elif role == 'INVESTIGATOR':
        cases = IncidentCase.objects.filter(assigned_investigator=request.user)
    else:
        cases = IncidentCase.objects.all()

    total_cases = IncidentCase.objects.count()
    resolved_cases = IncidentCase.objects.filter(current_status='RESOLVED').count()
    critical_cases = IncidentCase.objects.filter(risk_level='CRITICAL').count()
    pending_approvals = UserProfile.objects.filter(is_approved=False, approval_status='PENDING_APPROVAL').count()

    # Platform breakdown analytics
    platforms = ['FACEBOOK', 'INSTAGRAM', 'LINKEDIN', 'TWITTER', 'TIKTOK']
    platform_stats = []
    for p in platforms:
        cnt = IncidentCase.objects.filter(platform=p).count()
        pct = int((cnt / total_cases) * 100) if total_cases > 0 else 0
        platform_stats.append({'name': p.title(), 'count': cnt, 'pct': pct})

    pending_users = UserProfile.objects.filter(is_approved=False, approval_status='PENDING_APPROVAL')[:5]
    investigators = UserProfile.objects.filter(role='INVESTIGATOR', is_approved=True)

    return render(request, 'portal_app/dashboard.html', {
        'cases': cases[:8],
        'total_cases': total_cases,
        'resolved_cases': resolved_cases,
        'critical_cases': critical_cases,
        'pending_approvals': pending_approvals,
        'platform_stats': platform_stats,
        'pending_users': pending_users,
        'investigators': investigators,
        'role': role,
    })


def submit_report_view(request):
    # Unified complaint submission capturing incident details, platform URL, and optional first evidence
    ensure_seed_data()
    initial = {}
    if request.user.is_authenticated:
        initial = {
            'reporter_name': request.user.first_name or request.user.username,
            'reporter_email': request.user.email,
        }

    if request.method == 'POST':
        form = IncidentSubmissionForm(request.POST)
        evidence_form = EvidenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            case_obj = form.save(commit=False)
            if request.user.is_authenticated:
                case_obj.reporter = request.user
            case_obj.save()

            # Save optional evidence file if attached on initial submission
            if request.FILES.get('file') and evidence_form.is_valid():
                ev = evidence_form.save(commit=False)
                ev.case = case_obj
                ev.uploaded_by = request.user if request.user.is_authenticated else None
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
                f"Report submitted! Case ID: {case_obj.case_id} | Tracking PIN: {case_obj.security_pin}. You may now upload additional evidence or verify your identity."
            )
            return redirect('case_detail', case_id=case_obj.case_id)
    else:
        form = IncidentSubmissionForm(initial=initial)
        evidence_form = EvidenceUploadForm()

    return render(request, 'portal_app/submit_report.html', {
        'form': form,
        'evidence_form': evidence_form,
    })


def case_list_view(request):
    # Filterable incident case directory
    ensure_seed_data()
    cases = IncidentCase.objects.select_related('assigned_investigator').all()

    if request.user.is_authenticated and request.user.profile.role == 'CITIZEN':
        cases = cases.filter(Q(reporter=request.user) | Q(reporter_email=request.user.email))

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


def case_detail_view(request, case_id):
    # Unified All-in-One Case Hub: Evidence, ID Verification, Triage, Assignment, and Investigation Journal
    case = get_object_or_404(IncidentCase.objects.select_related('assigned_investigator'), case_id=case_id)
    evidences = case.evidences.all()
    verifications = case.verifications.all()
    notes = case.notes.all()

    user_role = request.user.profile.role if request.user.is_authenticated and hasattr(request.user, 'profile') else 'CITIZEN'
    is_staff_role = user_role in ['ADMIN', 'INVESTIGATOR']

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
            evidence_form = EvidenceUploadForm(request.POST, request.FILES)
            if evidence_form.is_valid():
                ev = evidence_form.save(commit=False)
                ev.case = case
                ev.uploaded_by = request.user if request.user.is_authenticated else None
                ev.save()
                log_audit_event(request, case, 'EVIDENCE_UPLOADED', case.current_status, case.current_status, f"Uploaded evidence file ({ev.get_file_type_display()}).")
                messages.success(request, "Supporting evidence uploaded and validated.")
                return redirect('case_detail', case_id=case.case_id)

        elif action == 'SUBMIT_VERIFICATION':
            verify_form = IdentityVerificationForm(request.POST, request.FILES)
            if verify_form.is_valid():
                ver = verify_form.save(commit=False)
                ver.case = case
                ver.save()
                log_audit_event(request, case, 'IDENTITY_SUBMITTED', case.current_status, 'PENDING_VERIFICATION', f"Identity verification submitted by {ver.reporter_full_name}.")
                messages.success(request, f"Identity documents submitted. Token: {ver.verification_token}")
                return redirect('case_detail', case_id=case.case_id)

        elif action == 'VERIFY_DECISION' and user_role == 'ADMIN':
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
            log_audit_event(request, case, 'IDENTITY_VERIFIED', 'PENDING', ver_obj.verification_status, f"Admin {request.user.username} marked ID verification as {ver_obj.verification_status}.")
            messages.success(request, f"Identity verification marked as {ver_obj.verification_status}.")
            return redirect('case_detail', case_id=case.case_id)

        elif action == 'SAVE_TRIAGE' and user_role == 'ADMIN':
            triage_form = CaseTriageReviewForm(request.POST, instance=case)
            if triage_form.is_valid():
                old_status = case.current_status
                obj = triage_form.save(commit=False)
                obj.reviewed_by = request.user.first_name or request.user.username
                obj.reviewed_at = timezone.now()
                obj.save()
                log_audit_event(request, case, 'CASE_TRIAGED', old_status, obj.current_status, f"Risk assessed as {obj.risk_level}; status set to {obj.current_status}.")
                messages.success(request, "Administrative triage assessment saved.")
                return redirect('case_detail', case_id=case.case_id)

        elif action == 'ASSIGN_INVESTIGATOR' and user_role == 'ADMIN':
            assign_form = CaseAssignmentForm(request.POST, instance=case)
            if assign_form.is_valid():
                old_status = case.current_status
                obj = assign_form.save(commit=False)
                if obj.assigned_investigator:
                    obj.assigned_at = timezone.now()
                    if obj.current_status in ['SUBMITTED', 'IDENTITY_VERIFIED', 'EVIDENCE_ACCEPTED']:
                        obj.current_status = 'ASSIGNED'
                    obj.public_status_message = f"Case assigned to Investigator {obj.assigned_investigator.first_name or obj.assigned_investigator.username}."
                obj.save()
                send_case_notification(
                    case, case.reporter, case.reporter_email, 'SMS',
                    f"Investigator Assigned: {case.case_id}",
                    obj.public_status_message
                )
                log_audit_event(request, case, 'ASSIGNED_TO_OFFICER', old_status, obj.current_status, f"Assigned to {obj.assigned_investigator.username if obj.assigned_investigator else 'Unassigned'}.")
                messages.success(request, "Investigator assigned successfully.")
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
                log_audit_event(request, case, 'STATUS_TRANSITION', old_status, obj.current_status, f"Investigation status updated to {obj.current_status}.")
                messages.success(request, "Investigation progress updated.")
                return redirect('case_detail', case_id=case.case_id)

        elif action == 'ADD_NOTE' and is_staff_role:
            note_form = InvestigationNoteForm(request.POST)
            if note_form.is_valid():
                n = note_form.save(commit=False)
                n.case = case
                n.officer_name = request.user.first_name or request.user.username
                n.save()
                log_audit_event(request, case, 'NOTE_LOGGED', case.current_status, case.current_status, f"Added {n.get_note_type_display()} note.")
                messages.success(request, "Forensic note added to case journal.")
                return redirect('case_detail', case_id=case.case_id)

    return render(request, 'portal_app/case_detail.html', {
        'case': case,
        'evidences': evidences,
        'verifications': verifications,
        'notes': notes,
        'user_role': user_role,
        'is_staff_role': is_staff_role,
        'evidence_form': evidence_form,
        'verify_form': verify_form,
        'triage_form': triage_form,
        'assign_form': assign_form,
        'progress_form': progress_form,
        'note_form': note_form,
    })


def public_tracker_view(request):
    # Public citizen case status tracker by Case ID and 6-digit Security PIN
    ensure_seed_data()
    case_id_q = request.GET.get('case_id', '').strip().upper()
    pin_q = request.GET.get('pin', '').strip()
    found_case = None
    searched = False

    if case_id_q:
        searched = True
        try:
            obj = IncidentCase.objects.get(case_id=case_id_q)
            if pin_q and obj.security_pin != pin_q:
                messages.error(request, "Invalid Security Verification PIN for this case.")
            else:
                found_case = obj
        except IncidentCase.DoesNotExist:
            messages.warning(request, f"No case found with ID '{case_id_q}'.")

    sample_cases = IncidentCase.objects.all()[:3]
    return render(request, 'portal_app/tracker.html', {
        'case': found_case,
        'searched': searched,
        'case_id_q': case_id_q,
        'pin_q': pin_q,
        'sample_cases': sample_cases,
    })


@login_required
def notifications_view(request):
    # Notification inbox filtered by role/user
    if request.user.profile.role in ['ADMIN', 'INVESTIGATOR']:
        alerts = CaseEventNotification.objects.all()
    else:
        alerts = CaseEventNotification.objects.filter(
            Q(recipient=request.user) | Q(recipient_email=request.user.email)
        )

    channel_f = request.GET.get('channel', '')
    if channel_f:
        alerts = alerts.filter(channel=channel_f)

    return render(request, 'portal_app/notifications.html', {
        'alerts': alerts,
        'channel_f': channel_f,
    })


@login_required
def mark_notification_read_view(request, notif_id):
    alert = get_object_or_404(CaseEventNotification, id=notif_id)
    alert.is_read = True
    alert.save()
    return redirect('notifications')


@login_required
def audit_logs_view(request):
    # Security audit history log with SHA-256 verification and CSV export
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


@login_required
def governance_approvals_view(request):
    # Dedicated Administrative User Approval Console (Approve / Reject / Suspend sign-ups)
    if request.user.profile.role != 'ADMIN':
        messages.error(request, "Only System Administrators can access the User Governance Panel.")
        return redirect('dashboard')

    status_f = request.GET.get('status', 'ALL')
    profiles = UserProfile.objects.select_related('user').all().order_by('-created_at')
    if status_f != 'ALL':
        profiles = profiles.filter(approval_status=status_f)

    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')
        target = get_object_or_404(UserProfile, id=profile_id)

        if action == 'APPROVE':
            target.is_approved = True
            target.approval_status = 'APPROVED'
            target.approved_by = request.user.username
            target.approved_at = timezone.now()
            target.approval_notes = 'Account approved for system access.'
            target.save()
            log_audit_event(request, None, 'USER_APPROVED', 'PENDING', 'APPROVED', f"Admin approved user '{target.user.username}'.")
            messages.success(request, f"Account '{target.user.username}' APPROVED. Login access is now active.")
        elif action == 'REJECT':
            target.is_approved = False
            target.approval_status = 'REJECTED'
            target.approval_notes = 'Registration declined by administrator.'
            target.save()
            log_audit_event(request, None, 'USER_REJECTED', 'PENDING', 'REJECTED', f"Admin rejected user '{target.user.username}'.")
            messages.warning(request, f"Account '{target.user.username}' has been REJECTED.")
        elif action == 'SUSPEND':
            target.is_approved = False
            target.approval_status = 'SUSPENDED'
            target.approval_notes = 'Account suspended by administrator.'
            target.save()
            log_audit_event(request, None, 'USER_SUSPENDED', 'APPROVED', 'SUSPENDED', f"Admin suspended user '{target.user.username}'.")
            messages.error(request, f"Account '{target.user.username}' has been SUSPENDED.")

        return redirect('governance_approvals')

    return render(request, 'portal_app/governance_approvals.html', {
        'profiles': profiles,
        'status_f': status_f,
    })
