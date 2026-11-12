from django.shortcuts import render, get_object_or_404
from .models import PlatformReport

def platform_list_view(request):
    """
    Dedicated View for listing all registered platform reports.
    """
    reports = PlatformReport.objects.all()
    return render(request, 'platform_app/platform_list.html', {
        'reports': reports,
        'title': 'Reported Profile URLs'
    })

def platform_case_detail_view(request, case_id):
    """
    Dedicated View rendering verified platform link and target account handle.
    """
    report = get_object_or_404(PlatformReport, case_id=case_id)
    return render(request, 'platform_app/platform_case_detail.html', {
        'report': report,
        'title': f"Platform Details: {report.case_id}"
    })

