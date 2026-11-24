# Forms for status updates and logging notes
from django import forms
from .models import InvestigationCase, InvestigationNoteEntry

class CaseStatusUpdateForm(forms.ModelForm):
    # Form to advance workflow status and suspect information
    class Meta:
        model = InvestigationCase
        fields = [
            'current_status',
            'suspect_lead_info',
            'platform_takedown_requested',
            'platform_ticket_id',
        ]
        widgets = {
            'current_status': forms.Select(attrs={'class': 'form-select'}),
            'suspect_lead_info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter identified IP addresses, proxy VPN logs, or associated financial IDs...'
            }),
            'platform_takedown_requested': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'platform_ticket_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. META-LEGAL-294819'}),
        }


class AddInvestigationNoteForm(forms.ModelForm):
    # Form to append timestamped investigation journal entries
    class Meta:
        model = InvestigationNoteEntry
        fields = ['officer_name', 'note_type', 'is_confidential', 'detailed_notes']
        widgets = {
            'officer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inspector Sarwar'}),
            'note_type': forms.Select(attrs={'class': 'form-select'}),
            'is_confidential': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'detailed_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Document forensic observations, digital fingerprinting results, or witness interview summaries...'
            }),
        }
