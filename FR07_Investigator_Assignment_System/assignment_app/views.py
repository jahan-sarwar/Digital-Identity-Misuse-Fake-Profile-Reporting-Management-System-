# Views managing investigator assignment and workload allocation
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import CaseAssignment, InvestigatorStaff
from .forms import CaseAssignmentForm

def populate_seed_data():
    # Helper to generate investigators and sample cases if empty
    if not InvestigatorStaff.objects.exists():
        i1 = InvestigatorStaff.objects.create(
            full_name='Inspector Sarwar Jahan',
            badge_number='CID-CYBER-014',
            email='sarwar.cid@police.gov.bd',
            phone='+880 1718-000014',
            rank_title='Lead Cyber Forensic Detective',
            specialization='SOCIAL_MEDIA_FRAUD',
            active_caseload=2,
            max_caseload_capacity=5,
            is_available=True
        )
        i2 = InvestigatorStaff.objects.create(
            full_name='Sub-Inspector Ariful Islam',
            badge_number='CID-CYBER-080',
            email='ariful.cid@police.gov.bd',
            phone='+880 1718-000080',
            rank_title='Digital Forensics Specialist',
            specialization='CYBER_EXTORTION',
            active_caseload=3,
            max_caseload_capacity=5,
            is_available=True
        )
        i3 = InvestigatorStaff.objects.create(
            full_name='Sub-Inspector Bishal Krisna Paul',
            badge_number='CID-CYBER-075',
            email='bishal.cid@police.gov.bd',
            phone='+880 1718-000075',
            rank_title='Social Media OSINT Analyst',
            specialization='CORPORATE_IDENTITY_THEFT',
            active_caseload=1,
            max_caseload_capacity=4,
            is_available=True
        )

        CaseAssignment.objects.create(
            case_id='CASE-2026-9001',
            title='Fake Medical Doctor Profile Soliciting Funds on Facebook',
            platform='Facebook',
            priority='URGENT',
            assignment_status='UNASSIGNED',
            assigned_by='Supervisory Desk'
        )
        CaseAssignment.objects.create(
            case_id='CASE-2026-9002',
            title='Corporate Executive LinkedIn Cloned for Financial Phishing',
            platform='LinkedIn',
            priority='HIGH',
            assignment_status='ASSIGNED',
            assigned_investigator=i1,
            assigned_by='Admin Sarwar',
            assigned_at=timezone.now(),
            supervisor_directives='Trace originating IP from login headers and file emergency takedown request.'
        )
        CaseAssignment.objects.create(
            case_id='CASE-2026-9003',
            title='Instagram Fashion Boutique Impersonation & Slander',
            platform='Instagram',
            priority='MEDIUM',
            assignment_status='UNASSIGNED',
            assigned_by='Supervisory Desk'
        )


def assignment_dashboard_view(request):
    # Ensure seed officers and cases are populated
    populate_seed_data()

    # Query investigators and open case assignments
    investigators = InvestigatorStaff.objects.all()
    assignments = CaseAssignment.objects.all()

    # Optional filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        assignments = assignments.filter(assignment_status=status_filter)

    # Compute key administrative metrics
    total_cases = CaseAssignment.objects.count()
    unassigned_cases = CaseAssignment.objects.filter(assignment_status='UNASSIGNED').count()
    assigned_cases = CaseAssignment.objects.filter(assignment_status='ASSIGNED').count()
    total_investigators = investigators.count()

    context = {
        'investigators': investigators,
        'assignments': assignments,
        'total_cases': total_cases,
        'unassigned_cases': unassigned_cases,
        'assigned_cases': assigned_cases,
        'total_investigators': total_investigators,
        'selected_status': status_filter or 'ALL',
    }
    return render(request, 'assignment_app/assignment_dashboard.html', context)


def assign_case_view(request, case_id):
    # Retrieve specific case to assign
    case = get_object_or_404(CaseAssignment, case_id=case_id)

    if request.method == 'POST':
        form = CaseAssignmentForm(request.POST, instance=case)
        if form.is_valid():
            assignment_obj = form.save(commit=False)
            assignment_obj.assignment_status = 'ASSIGNED'
            assignment_obj.assigned_at = timezone.now()
            assignment_obj.save()

            # Increment active caseload count for assigned investigator
            officer = assignment_obj.assigned_investigator
            if officer:
                officer.active_caseload += 1
                if officer.active_caseload >= officer.max_caseload_capacity:
                    officer.is_available = False
                officer.save()

            messages.success(
                request,
                f"Case {case.case_id} successfully assigned to {officer.full_name} ({officer.badge_number})."
            )
            return redirect('assignment_dashboard')
    else:
        form = CaseAssignmentForm(instance=case)

    return render(request, 'assignment_app/assign_case.html', {
        'case': case,
        'form': form
    })
