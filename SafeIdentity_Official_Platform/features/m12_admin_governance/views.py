# Module 12: Executive Administrative Dashboard & User Approval Governance
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from portal_app.models import UserProfile, IncidentCase
from portal_app.seed import ensure_seed_data
from features.common import log_audit_event


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
