# Views for Administrative Dashboard, User Approval, and Access Control
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import SystemUserAccount, AdministrativeCaseMetric
from .forms import UserRegistrationForm, UserLoginForm

def populate_seed_admin_data():
    # Helper to generate seed users and metrics
    if not SystemUserAccount.objects.exists():
        admin_user = SystemUserAccount.objects.create(
            username='admin.sarwar',
            full_name='Chief Administrator Sarwar Jahan',
            email='admin.sarwar@cyberdefense.gov.bd',
            phone='+880 1718-000014',
            assigned_role='SYSTEM_ADMINISTRATOR',
            department='Cyber Command Headquarters',
            is_approved=True,
            approval_status='APPROVED',
            approved_by='Head of Agency',
            admin_approval_notes='Master administrative superuser authorization granted.'
        )
        admin_user.set_password('Admin@1234')
        admin_user.save()

        pending_officer = SystemUserAccount.objects.create(
            username='officer.ariful',
            full_name='Sub-Inspector Ariful Islam',
            email='ariful.islam@police.gov.bd',
            phone='+880 1718-000080',
            assigned_role='FORENSIC_INVESTIGATOR',
            department='Digital Forensics Laboratory',
            is_approved=False,
            approval_status='PENDING_APPROVAL',
            admin_approval_notes='Awaiting credentials verification by Security Admin.'
        )
        pending_officer.set_password('Officer@1234')
        pending_officer.save()

        pending_citizen = SystemUserAccount.objects.create(
            username='citizen.ayesha',
            full_name='Ayesha Siddiqua',
            email='ayesha.s@example.com',
            phone='+880 1819-000111',
            assigned_role='CITIZEN_REPORTER',
            department='General Public',
            is_approved=False,
            approval_status='PENDING_APPROVAL',
            admin_approval_notes='New public complainant registration.'
        )
        pending_citizen.set_password('User@1234')
        pending_citizen.save()


def admin_dashboard_overview_view(request):
    # Ensure seed users and stats exist
    populate_seed_admin_data()

    # Calculate system KPIs
    total_users = SystemUserAccount.objects.count()
    pending_approvals = SystemUserAccount.objects.filter(is_approved=False, approval_status='PENDING_APPROVAL').count()
    approved_users = SystemUserAccount.objects.filter(is_approved=True).count()
    investigators_count = SystemUserAccount.objects.filter(assigned_role='FORENSIC_INVESTIGATOR').count()

    # Pre-calculated case breakdown metrics
    case_stats = {
        'total_cases': 48,
        'active_investigations': 19,
        'takedowns_issued': 21,
        'resolved_cases': 24,
        'resolution_rate': 78,
    }

    # Platform distribution
    platform_breakdown = [
        {'platform': 'Facebook', 'count': 26, 'percentage': 54},
        {'platform': 'Instagram', 'count': 12, 'percentage': 25},
        {'platform': 'LinkedIn', 'count': 6, 'percentage': 13},
        {'platform': 'TikTok / Other', 'count': 4, 'percentage': 8},
    ]

    recent_pending = SystemUserAccount.objects.filter(is_approved=False)[:5]

    context = {
        'total_users': total_users,
        'pending_approvals': pending_approvals,
        'approved_users': approved_users,
        'investigators_count': investigators_count,
        'case_stats': case_stats,
        'platform_breakdown': platform_breakdown,
        'recent_pending': recent_pending,
    }
    return render(request, 'dashboard_app/admin_dashboard.html', context)


def user_approval_queue_view(request):
    # View to inspect all registration requests and approve/reject users
    populate_seed_admin_data()

    status_filter = request.GET.get('status', 'PENDING_APPROVAL')
    users = SystemUserAccount.objects.all()

    if status_filter != 'ALL':
        users = users.filter(approval_status=status_filter)

    # Process Admin Approval
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')

        target_user = get_object_or_404(SystemUserAccount, id=user_id)
        if action == 'APPROVE':
            # Grant official login approval
            target_user.is_approved = True
            target_user.approval_status = 'APPROVED'
            target_user.approved_by = 'Administrator Sarwar'
            target_user.admin_approval_notes = admin_notes or 'Account authorized by Security Administrator.'
            target_user.approved_at = timezone.now()
            target_user.save()
            messages.success(request, f"User '{target_user.username}' ({target_user.full_name}) has been officially APPROVED. Login access is now unlocked.")
        elif action == 'REJECT':
            # Reject application
            target_user.is_approved = False
            target_user.approval_status = 'REJECTED'
            target_user.approved_by = 'Administrator Sarwar'
            target_user.admin_approval_notes = admin_notes or 'Registration rejected due to invalid credentials.'
            target_user.save()
            messages.warning(request, f"User '{target_user.username}' registration application has been REJECTED.")
        elif action == 'SUSPEND':
            # Suspend active user
            target_user.is_approved = False
            target_user.approval_status = 'SUSPENDED'
            target_user.admin_approval_notes = admin_notes or 'Account suspended by administrator.'
            target_user.save()
            messages.error(request, f"User '{target_user.username}' account access has been SUSPENDED.")

        return redirect('user_approval_queue')

    return render(request, 'dashboard_app/user_approval_queue.html', {
        'users': users,
        'selected_status': status_filter,
    })


def user_signup_view(request):
    # View for citizens and officers to register an account
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_obj = form.save(commit=False)
            # Newly registered accounts are locked pending admin approval
            user_obj.is_approved = False
            user_obj.approval_status = 'PENDING_APPROVAL'
            user_obj.set_password(form.cleaned_data['password'])
            user_obj.save()

            messages.success(
                request,
                f"Registration submitted for '{user_obj.username}'. Your account is currently PENDING ADMINISTRATIVE APPROVAL before you can log in."
            )
            return redirect('user_login')
    else:
        form = UserRegistrationForm()

    return render(request, 'dashboard_app/signup.html', {'form': form})


def user_login_view(request):
    # View to authenticate users with strict approval enforcement
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pwd = form.cleaned_data['password']

            # Lookup by username or email
            user_match = SystemUserAccount.objects.filter(username=uname).first() or SystemUserAccount.objects.filter(email=uname).first()
            if user_match and user_match.check_password(pwd):
                # Critical Check: Is account approved by Security Admin?
                if not user_match.is_approved:
                    messages.error(
                        request,
                        f"ACCESS DENIED: Account '{user_match.username}' is currently PENDING ADMINISTRATIVE APPROVAL. Please await verification from the Security Admin."
                    )
                else:
                    messages.success(
                        request,
                        f"Welcome back, {user_match.full_name}! Successfully logged in with role [{user_match.get_assigned_role_display()}]."
                    )
                    return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid username or password credentials.")
    else:
        form = UserLoginForm()

    return render(request, 'dashboard_app/login.html', {'form': form})
