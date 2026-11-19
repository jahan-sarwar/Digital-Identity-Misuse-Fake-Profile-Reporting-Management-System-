from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import UserProfile, CaseReportRequest

def is_admin_or_staff(user):
    # Check if the user is authorized administrator or staff / ইউজার অ্যাডমিন বা স্টাফ কি না তা যাচাই
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin_or_staff, login_url='login')
def admin_portal_view(request):
    """
    Administrative Command Portal View / সেন্ট্রাল অ্যাডমিন কন্ট্রোল পোর্টাল ভিউ।
    Allows administrators to:
    1. Review and Accept/Approve pending user account registrations.
    2. Review and Accept/Dismiss submitted pending case reports.
    """
    # Fetch pending user registrations / অনুমোদনের অপেক্ষায় থাকা নতুন ইউজার তালিকা
    pending_users = UserProfile.objects.filter(approval_status='PENDING').select_related('user').order_by('-created_at')
    
    # Fetch approved user accounts / অনুমোদিত সক্রিয় ব্যবহারকারী তালিকা
    approved_users = UserProfile.objects.filter(approval_status='APPROVED').select_related('user').order_by('-created_at')
    
    # Fetch pending case requests awaiting acceptance / অনুমোদনের অপেক্ষায় থাকা পেন্ডিং কেস
    pending_cases = CaseReportRequest.objects.filter(status='PENDING').select_related('reporter').order_by('-created_at')
    
    # Fetch accepted and active cases / গৃহীত ও সক্রিয় কেসের তালিকা
    accepted_cases = CaseReportRequest.objects.filter(status='ACCEPTED').select_related('reporter').order_by('-created_at')

    context = {
        'title': 'Administration Management Portal',
        'pending_users': pending_users,
        'approved_users': approved_users,
        'pending_cases': pending_cases,
        'accepted_cases': accepted_cases,
        'pending_users_count': pending_users.count(),
        'approved_users_count': approved_users.count(),
        'pending_cases_count': pending_cases.count(),
        'accepted_cases_count': accepted_cases.count(),
    }
    return render(request, 'auth_app/admin_portal.html', context)

@login_required
@user_passes_test(is_admin_or_staff, login_url='login')
def approve_user_account(request, user_id):
    """
    Accept & Approve User Account / ব্যবহারকারী অ্যাকাউন্ট অনুমোদন ও সক্রিয়করণ।
    Transitions user from PENDING to APPROVED and enables login access.
    """
    target_user = get_object_or_404(User, id=user_id)
    profile = target_user.profile
    profile.approval_status = 'APPROVED'
    profile.approved_by = request.user
    profile.approval_date = timezone.now()
    profile.save()

    # Activate Django user for authentication / লগইন সক্রিয়করণ
    target_user.is_active = True
    target_user.save()

    messages.success(request, f"User account '{target_user.username}' has been successfully approved and activated. (অ্যাকাউন্ট সফলভাবে অনুমোদন করা হয়েছে)")
    return redirect('admin_portal')

@login_required
@user_passes_test(is_admin_or_staff, login_url='login')
def reject_user_account(request, user_id):
    """
    Reject User Account Registration / ব্যবহারকারী অ্যাকাউন্ট আবেদন বাতিলকরণ।
    """
    target_user = get_object_or_404(User, id=user_id)
    profile = target_user.profile
    profile.approval_status = 'REJECTED'
    profile.approved_by = request.user
    profile.approval_date = timezone.now()
    profile.save()

    # Disable Django user login / লগইন নিষ্ক্রিয়করণ
    target_user.is_active = False
    target_user.save()

    messages.warning(request, f"User registration for '{target_user.username}' has been rejected. (অ্যাকাউন্ট আবেদনটি বাতিল করা হয়েছে)")
    return redirect('admin_portal')

@login_required
@user_passes_test(is_admin_or_staff, login_url='login')
def accept_case_request(request, case_id):
    """
    Accept Pending Case Request / পেন্ডিং কেস রিকোয়েস্ট গ্রহণ ও অনুমোদন।
    Transitions case to ACCEPTED status so investigators can take actions.
    """
    case = get_object_or_404(CaseReportRequest, id=case_id)
    case.status = 'ACCEPTED'
    case.reviewed_by = request.user
    case.reviewed_at = timezone.now()
    admin_note = request.POST.get('admin_notes', 'Case verified and accepted into active investigation.')
    case.admin_notes = admin_note
    case.save()

    messages.success(request, f"Case #{case.case_number} has been accepted and moved to active investigation. (কেস সফলভাবে গ্রহণ করা হয়েছে)")
    return redirect('admin_portal')

@login_required
@user_passes_test(is_admin_or_staff, login_url='login')
def reject_case_request(request, case_id):
    """
    Reject / Dismiss Pending Case Request / কেস রিকোয়েস্ট খারিজ বা বাতিলকরণ।
    """
    case = get_object_or_404(CaseReportRequest, id=case_id)
    case.status = 'REJECTED'
    case.reviewed_by = request.user
    case.reviewed_at = timezone.now()
    admin_note = request.POST.get('admin_notes', 'Case rejected due to insufficient initial evidence.')
    case.admin_notes = admin_note
    case.save()

    messages.info(request, f"Case #{case.case_number} has been dismissed/rejected. (কেস বাতিল করা হয়েছে)")
    return redirect('admin_portal')

@login_required
def submit_case_view(request):
    """
    Submit Case Complaint View / সাধারণ ব্যবহারকারীর কেস দাখিল করার ভিউ।
    """
    if request.method == 'POST':
        platform = request.POST.get('platform')
        fake_profile_url = request.POST.get('fake_profile_url')
        incident_description = request.POST.get('incident_description')
        evidence_notes = request.POST.get('evidence_notes', '')

        # Generate unique case tracking ID / ইউনিক কেস নম্বর তৈরি
        import uuid
        case_number = f"CASE-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"

        case = CaseReportRequest.objects.create(
            reporter=request.user,
            case_number=case_number,
            platform=platform,
            fake_profile_url=fake_profile_url,
            incident_description=incident_description,
            evidence_notes=evidence_notes,
            status='PENDING'
        )
        messages.success(request, f"Your case #{case.case_number} has been submitted! It is now pending administrator review. (আপনার কেসটি দাখিল হয়েছে এবং অ্যাডমিন পর্যালোচনার অপেক্ষায় রয়েছে)")
        return redirect('profile')

    return render(request, 'auth_app/submit_case.html', {
        'title': 'Submit Identity Misuse Complaint'
    })
