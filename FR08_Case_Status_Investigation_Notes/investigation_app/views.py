# Views controlling case status transitions and investigation journal logs
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import InvestigationCase, InvestigationNoteEntry
from .forms import CaseStatusUpdateForm, AddInvestigationNoteForm

def populate_seed_investigation():
    # Helper to generate an active investigation case with journal entries
    if not InvestigationCase.objects.exists():
        case = InvestigationCase.objects.create(
            case_id='CASE-2026-8801',
            case_title='Impersonation of University Faculty to Defraud Students',
            victim_name='Prof. Dr. Sarwar Jahan',
            investigating_officer='Lead Detective Sarwar',
            current_status='IN_PROGRESS',
            suspect_lead_info='Offender active from dynamic IP subnet 103.205.x.x (Mobile ISP). Registered with disposable email.',
            platform_takedown_requested=True,
            platform_ticket_id='FB-LEGAL-77291-BD'
        )
        InvestigationNoteEntry.objects.create(
            case=case,
            officer_name='Lead Detective Sarwar',
            note_type='STATUS_CHANGE',
            previous_status='ASSIGNED',
            new_status='IN_PROGRESS',
            detailed_notes='Case accepted and formal investigation initiated. Digital screenshot evidence verified and cryptographic hashes computed.'
        )
        InvestigationNoteEntry.objects.create(
            case=case,
            officer_name='Lead Detective Sarwar',
            note_type='FORENSIC_EXAMINATION',
            detailed_notes='Metadata extraction from impersonation screenshots confirms image cloning from official university department website directory.'
        )
        InvestigationNoteEntry.objects.create(
            case=case,
            officer_name='Lead Detective Sarwar',
            note_type='PLATFORM_CORRESPONDENCE',
            detailed_notes='Submitted expedited takedown subpoena under Bangladesh Cyber Security regulatory framework to Meta Emergency Response Unit.'
        )


def case_journal_list_view(request):
    # Ensure seed cases exist
    populate_seed_investigation()

    # Retrieve all ongoing investigations
    cases = InvestigationCase.objects.all()
    
    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        cases = cases.filter(current_status=status_filter)

    # Statistics counters
    total_active = InvestigationCase.objects.count()
    in_progress = InvestigationCase.objects.filter(current_status='IN_PROGRESS').count()
    escalated = InvestigationCase.objects.filter(current_status='ESCALATED_TO_PLATFORM').count()
    resolved = InvestigationCase.objects.filter(current_status='RESOLVED').count()

    context = {
        'cases': cases,
        'total_active': total_active,
        'in_progress': in_progress,
        'escalated': escalated,
        'resolved': resolved,
        'selected_status': status_filter or 'ALL',
    }
    return render(request, 'investigation_app/case_journal_list.html', context)


def update_investigation_view(request, case_id):
    # Retrieve investigation case by ID
    case = get_object_or_404(InvestigationCase, case_id=case_id)
    notes = case.investigation_notes.all()

    status_form = CaseStatusUpdateForm(instance=case)
    note_form = AddInvestigationNoteForm()

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        # Action: Update Case Status & Lead Info
        if action_type == 'UPDATE_STATUS':
            old_status = case.current_status
            status_form = CaseStatusUpdateForm(request.POST, instance=case)
            if status_form.is_valid():
                updated_case = status_form.save()
                new_status = updated_case.current_status
                
                # Automatically log status transition entry if changed
                if old_status != new_status:
                    InvestigationNoteEntry.objects.create(
                        case=case,
                        officer_name=case.investigating_officer,
                        note_type='STATUS_CHANGE',
                        previous_status=old_status,
                        new_status=new_status,
                        detailed_notes=f"Investigation status transitioned from [{old_status}] to [{new_status}]."
                    )
                messages.success(request, f"Case {case.case_id} status updated to {updated_case.get_current_status_display()}.")
                return redirect('update_investigation', case_id=case.case_id)

        # Action: Append New Investigation Note
        elif action_type == 'ADD_NOTE':
            note_form = AddInvestigationNoteForm(request.POST)
            if note_form.is_valid():
                new_note = note_form.save(commit=False)
                new_note.case = case
                new_note.save()
                messages.success(request, "New investigation finding logged to journal.")
                return redirect('update_investigation', case_id=case.case_id)

    return render(request, 'investigation_app/update_investigation.html', {
        'case': case,
        'notes': notes,
        'status_form': status_form,
        'note_form': note_form,
    })
