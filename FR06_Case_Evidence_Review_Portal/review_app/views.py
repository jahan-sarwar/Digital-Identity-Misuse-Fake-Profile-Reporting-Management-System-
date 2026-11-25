# Views managing case evidence triage and review
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import IncidentReviewCase
from .forms import CaseReviewDecisionForm

def populate_seed_cases():
    # Helper to seed realistic cases for demonstration
    if not IncidentReviewCase.objects.exists():
        IncidentReviewCase.objects.create(
            case_id='CASE-2026-1042',
            complainant_name='Sarwar Jahan',
            complainant_email='sarwar.jahan@example.com',
            target_platform='FACEBOOK',
            fake_profile_url='https://facebook.com/fake.sarwar.profile.official',
            impersonated_name='Sarwar Jahan (Official Fraud Account)',
            incident_narrative='The perpetrator created a clone profile using my real photographs and national credentials, actively soliciting money from university colleagues claiming emergency medical assistance.',
            risk_level='CRITICAL',
            review_status='PENDING_TRIAGE',
            evidence_count=3,
            evidence_summary='2 Profile Screenshots, 1 Bank Transfer Request Chat Screenshot'
        )
        IncidentReviewCase.objects.create(
            case_id='CASE-2026-1043',
            complainant_name='Ayesha Siddiqua',
            complainant_email='ayesha.s@example.com',
            target_platform='INSTAGRAM',
            fake_profile_url='https://instagram.com/ayesha_fashion_brand_official',
            impersonated_name='Ayesha Boutique Collection',
            incident_narrative='Fraudulent merchant Instagram handle created using victim brand trademarks, taking advance bKash payments without delivering clothing items.',
            risk_level='HIGH',
            review_status='EVIDENCE_ACCEPTED',
            evidence_count=2,
            evidence_summary='Fake Instagram Bio Screenshot, Customer Payment Slips',
            reviewer_notes='Trademark and visual identity theft confirmed. Evidence validated.',
            reviewed_by='Officer Sarwar'
        )
        IncidentReviewCase.objects.create(
            case_id='CASE-2026-1044',
            complainant_name='Tanvir Ahmed',
            complainant_email='tanvir.ahmed@example.com',
            target_platform='LINKEDIN',
            fake_profile_url='https://linkedin.com/in/fake-tanvir-software-lead',
            impersonated_name='Tanvir Ahmed Lead Consultant',
            incident_narrative='Fake LinkedIn profile impersonating executive role to gather sensitive company intelligence.',
            risk_level='MEDIUM',
            review_status='PENDING_TRIAGE',
            evidence_count=1,
            evidence_summary='LinkedIn URL & Profile PDF snapshot'
        )


def case_review_list_view(request):
    # Ensure seed cases exist
    populate_seed_cases()

    # Query all submitted incident cases
    cases = IncidentReviewCase.objects.all()

    # Apply filter parameters
    status_filter = request.GET.get('status')
    risk_filter = request.GET.get('risk')
    search_query = request.GET.get('q')

    if status_filter:
        cases = cases.filter(review_status=status_filter)
    if risk_filter:
        cases = cases.filter(risk_level=risk_filter)
    if search_query:
        cases = cases.filter(case_id__icontains=search_query) | cases.filter(complainant_name__icontains=search_query)

    # Statistics calculation for header cards
    total_count = IncidentReviewCase.objects.count()
    pending_count = IncidentReviewCase.objects.filter(review_status='PENDING_TRIAGE').count()
    critical_count = IncidentReviewCase.objects.filter(risk_level='CRITICAL').count()
    accepted_count = IncidentReviewCase.objects.filter(review_status='EVIDENCE_ACCEPTED').count()

    context = {
        'cases': cases,
        'total_count': total_count,
        'pending_count': pending_count,
        'critical_count': critical_count,
        'accepted_count': accepted_count,
        'selected_status': status_filter or '',
        'selected_risk': risk_filter or '',
        'search_query': search_query or '',
    }
    return render(request, 'review_app/case_list.html', context)


def case_detail_review_view(request, case_id):
    # Retrieve specific case
    case = get_object_or_404(IncidentReviewCase, case_id=case_id)

    # Handle administrative triage verdict submission
    if request.method == 'POST':
        form = CaseReviewDecisionForm(request.POST, instance=case)
        if form.is_valid():
            review_obj = form.save(commit=False)
            review_obj.reviewed_at = timezone.now()
            if not review_obj.reviewed_by:
                review_obj.reviewed_by = 'Inspector Sarwar'
            review_obj.save()
            messages.success(request, f"Case {case.case_id} evaluation updated successfully.")
            return redirect('case_detail_review', case_id=case.case_id)
    else:
        form = CaseReviewDecisionForm(instance=case)

    return render(request, 'review_app/case_detail_review.html', {
        'case': case,
        'form': form
    })
