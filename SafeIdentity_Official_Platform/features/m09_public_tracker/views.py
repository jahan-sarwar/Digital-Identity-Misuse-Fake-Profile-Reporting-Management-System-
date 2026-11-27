# Module 09: Public Case Status & Progress Tracker
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from portal_app.models import IncidentCase
from portal_app.seed import ensure_seed_data


@login_required
def public_tracker_view(request):
    # Track case progress by Case Reference ID and 6-digit Security PIN
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

    return render(request, 'portal_app/tracker.html', {
        'case': found_case,
        'searched': searched,
        'case_id_q': case_id_q,
        'pin_q': pin_q,
    })
