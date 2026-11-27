# Module 01: User Registration, Authentication & Account Profile Management
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from portal_app.forms import RegistrationForm, LoginForm, ProfileUpdateForm
from portal_app.seed import ensure_seed_data
from features.common import log_audit_event


def register_view(request):
    # Register a new citizen/investigator account in pending-approval state
    ensure_seed_data()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['full_name'],
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
    # Authenticate credentials with distinct Admin and Citizen login pathways
    ensure_seed_data()
    if request.user.is_authenticated:
        return redirect('dashboard')

    # Determine requested role tab: 'user' or 'admin'
    active_tab = request.POST.get('login_role') or request.GET.get('role', 'user')
    if active_tab not in ['user', 'admin']:
        active_tab = 'user'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']

            matched_user = User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()
            if matched_user:
                user = authenticate(request, username=matched_user.username, password=password)
                if user is not None:
                    # Role validation for Admin tab
                    is_admin_or_staff = (
                        user.is_superuser or 
                        user.is_staff or 
                        (hasattr(user, 'profile') and user.profile.role in ['ADMIN', 'INVESTIGATOR'])
                    )

                    if active_tab == 'admin' and not is_admin_or_staff:
                        messages.warning(
                            request,
                            f"Account '{user.username}' is a Citizen account. Please switch to the 'Citizen / General User' tab to sign in."
                        )
                    elif not user.profile.is_approved:
                        messages.error(
                            request,
                            f"ACCESS DENIED: Account '{user.username}' is currently {user.profile.get_approval_status_display()}. Please wait for Security Administrator approval."
                        )
                    else:
                        login(request, user)
                        log_audit_event(
                            request, None, 'USER_LOGIN', 'LOGGED_OUT', 'AUTHENTICATED',
                            f"User '{user.username}' signed in as {user.profile.get_role_display()} via {active_tab.upper()} portal."
                        )
                        messages.success(request, f"Welcome, {user.first_name or user.username}! Signed in as {user.profile.get_role_display()}.")
                        
                        if user.profile.role == 'ADMIN':
                            return redirect('dashboard')
                        return redirect('dashboard')
                else:
                    messages.error(request, "Invalid username or password. Please verify your credentials.")
            else:
                messages.error(request, "No account found matching this username or email.")
    else:
        form = LoginForm()

    return render(request, 'portal_app/login.html', {
        'form': form,
        'active_tab': active_tab,
    })


def logout_view(request):
    logout(request)
    messages.info(request, "You have been securely logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    # Manage user profile details and avatar
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
            'email': request.user.email
        })
    return render(request, 'portal_app/profile.html', {'form': form})
