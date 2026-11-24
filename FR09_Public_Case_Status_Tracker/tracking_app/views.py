# Views for Citizen Case Status Tracking Portal
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import TrackableCase

def populate_seed_trackable():
    # Helper to generate seed trackable cases if none exist
    if not TrackableCase.objects.exists():
        now = timezone.now().date()
        TrackableCase.objects.create(
            case_id='CASE-2026-7701',
            security_pin='123456',
            complainant_name='Sarwar Jahan',
            complainant_email='sarwar.jahan@example.com',
            platform_name='Facebook',
            impersonated_account_name='Sarwar Jahan (Fraud Clone)',
            progress_stage='4_INVESTIGATION',
            public_status_message='Digital forensics team has identified suspect ISP origin and issued an expedited legal removal notice to Meta Legal Operations.',
            assigned_agency='Cyber Crime Investigation Cell - Unit 7',
            estimated_completion_date=now + timedelta(days=2)
        )
        TrackableCase.objects.create(
            case_id='CASE-2026-7702',
            security_pin='654321',
            complainant_name='Amina Begum',
            complainant_email='amina.b@example.com',
            platform_name='Instagram',
            impersonated_account_name='Amina Begum Official Store',
            progress_stage='2_VERIFIED',
            public_status_message='Complainant National ID verified successfully. Case forwarded to supervisory desk for detective assignment.',
            assigned_agency='Digital Forensics Directorate',
            estimated_completion_date=now + timedelta(days=5)
        )
        TrackableCase.objects.create(
            case_id='CASE-2026-7703',
            security_pin='999888',
            complainant_name='Kazi Rafiqul',
            complainant_email='kazi.rafiq@example.com',
            platform_name='LinkedIn',
            impersonated_account_name='Kazi Rafiq Executive',
            progress_stage='5_RESOLVED',
            public_status_message='Fraudulent profile permanently deactivated by platform trust team. Case successfully closed.',
            assigned_agency='Cyber Incident Response Unit',
            estimated_completion_date=now - timedelta(days=1)
        )


def public_case_tracker_view(request):
    # Ensure seed cases exist
    populate_seed_trackable()

    searched = False
    found_case = None
    query_case_id = request.GET.get('case_id', '').strip().upper()
    query_pin = request.GET.get('pin', '').strip()

    # Look up case if Case ID provided
    if query_case_id:
        searched = True
        try:
            case_obj = TrackableCase.objects.get(case_id=query_case_id)
            if query_pin and case_obj.security_pin != query_pin:
                messages.error(request, "Invalid Security Verification PIN for this case reference.")
            else:
                found_case = case_obj
        except TrackableCase.DoesNotExist:
            messages.warning(request, f"No incident case found matching reference ID '{query_case_id}'.")

    recent_sample_cases = TrackableCase.objects.all()[:3]

    return render(request, 'tracking_app/tracker_home.html', {
        'searched': searched,
        'case': found_case,
        'query_case_id': query_case_id,
        'query_pin': query_pin,
        'sample_cases': recent_sample_cases,
    })
