# Views controlling identity verification workflows
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import IdentityVerification
from .forms import IdentityVerificationForm

def submit_verification_view(request):
    # Handle GET and POST requests for submitting identity verification
    if request.method == 'POST':
        # Bind incoming POST and FILES data
        form = IdentityVerificationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save verified record into SQLite database
            record = form.save()
            messages.success(
                request,
                f"Identity verification documents submitted successfully for Case {record.case_id}. Tracking Token: {record.verification_token}"
            )
            # Redirect to status tracking page
            return redirect('verification_status', token=record.verification_token)
        else:
            messages.error(request, "Please rectify the validation errors highlighted below.")
    else:
        # Prepopulate case_id if passed in GET query
        initial_data = {}
        case_id = request.GET.get('case_id')
        if case_id:
            initial_data['case_id'] = case_id
        form = IdentityVerificationForm(initial=initial_data)

    return render(request, 'verification_app/submit_verification.html', {'form': form})


def verification_status_view(request, token):
    # Look up identity verification record by UUID token
    record = get_object_or_404(IdentityVerification, verification_token=token)
    return render(request, 'verification_app/verification_status.html', {'record': record})


def verification_review_portal_view(request):
    # Administrative portal to inspect and verify identity documents
    records = IdentityVerification.objects.all()
    
    # Filter by verification status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        records = records.filter(verification_status=status_filter)

    # Process officer decision updates
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        action = request.POST.get('action')
        officer_name = request.POST.get('officer_name', 'Inspector Sarwar')
        notes = request.POST.get('notes', '')

        target_record = get_object_or_404(IdentityVerification, id=record_id)
        if action == 'APPROVE':
            # Mark document as verified
            target_record.verification_status = 'VERIFIED'
            target_record.admin_notes = notes or 'Identity documents fully authenticated against official records.'
            target_record.reviewed_by = officer_name
            target_record.reviewed_at = timezone.now()
            target_record.save()
            messages.success(request, f"Case {target_record.case_id} identity verified successfully.")
        elif action == 'REJECT':
            # Mark document as rejected
            reason = request.POST.get('reason', 'Document illegible or information mismatch.')
            target_record.verification_status = 'REJECTED'
            target_record.rejection_reason = reason
            target_record.admin_notes = notes
            target_record.reviewed_by = officer_name
            target_record.reviewed_at = timezone.now()
            target_record.save()
            messages.warning(request, f"Case {target_record.case_id} verification rejected.")
        return redirect('verification_review_portal')

    return render(request, 'verification_app/admin_review.html', {
        'records': records,
        'selected_status': status_filter or 'ALL'
    })
