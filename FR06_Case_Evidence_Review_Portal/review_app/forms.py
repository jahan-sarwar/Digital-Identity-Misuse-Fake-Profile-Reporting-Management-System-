# Forms for case review actions
from django import forms
from .models import IncidentReviewCase

class CaseReviewDecisionForm(forms.ModelForm):
    # Form mapping fields for administrative verdicts
    class Meta:
        model = IncidentReviewCase
        fields = ['risk_level', 'review_status', 'reviewer_notes', 'reviewed_by']
        widgets = {
            # Risk dropdown
            'risk_level': forms.Select(attrs={'class': 'form-select'}),
            # Review status dropdown
            'review_status': forms.Select(attrs={'class': 'form-select'}),
            # Reviewer comments
            'reviewer_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter comprehensive forensic review findings and operational recommendations...'
            }),
            # Reviewer officer signature
            'reviewed_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lead Officer Name'
            }),
        }
