from django.shortcuts import render, redirect
from django.contrib import messages
from .platform_forms import PlatformSubmissionForm

def submit_platform_url_view(request):
    """
    Dedicated View for submitting platform choice and profile URL.
    """
    if request.method == 'POST':
        form = PlatformSubmissionForm(request.POST)
        if form.is_valid():
            report = form.save()
            messages.success(request, f"Platform URL verified and filed! Case ID: {report.case_id}")
            return redirect('platform_case_detail', case_id=report.case_id)
        else:
            messages.error(request, "Validation failed. Please verify that the URL matches the selected platform.")
    else:
        form = PlatformSubmissionForm()

    return render(request, 'platform_app/submit_platform_url.html', {
        'form': form,
        'title': 'Submit Profile URL'
    })

