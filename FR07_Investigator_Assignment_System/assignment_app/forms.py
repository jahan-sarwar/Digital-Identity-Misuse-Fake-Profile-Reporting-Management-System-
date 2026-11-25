# Assignment forms
from AssignmentForm(forms.ModelForm):
    # Form to assign an officer to an open case
    class Meta:
        model = CaseAssignment
        fields = [
            'assigned_investigator',
            'priority',
            'deadline_date',
            'supervisor_directives',
            'assigned_by',
        ]
        widgets = {
            # Investigator selection dropdown
            'assigned_investigator': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            # Case priority tier
            'priority': forms.Select(attrs={'class': 'form-select'}),
            # Resolution deadline date picker
            'deadline_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # Directive instructions
            'supervisor_directives': forms.Texdjango import forms
from .models import CaseAssignment, InvestigatorStaff

class Casetarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Specify digital forensic priorities, platform escalation guidelines, or legal deadlines...'
            }),
            # Admin signer
            'assigned_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supervising Admin Name'}),
        }
