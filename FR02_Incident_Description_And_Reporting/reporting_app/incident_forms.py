from django import forms
from .models import IncidentReport

class IncidentSubmissionForm(forms.ModelForm):
    """
    FR-02: Dedicated form for submitting fake-profile / identity misuse incidents.
    Enforces minimum 30 characters in incident description and date validation.
    """
    class Meta:
        model = IncidentReport
        fields = [
            'reporter_name',
            'reporter_email',
            'incident_type',
            'title',
            'date_noticed',
            'incident_description',
            'impact_summary',
        ]
        widgets = {
            'reporter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'reporter_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'incident_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Fake account impersonating me on social network'}),
            'date_noticed': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'incident_description': forms.Textarea(attrs={
                'rows': 6,
                'class': 'form-control',
                'placeholder': 'Explain what occurred in detail. Mention what photos or personal bio were stolen, who was contacted, fraudulent actions attempted, etc. (Minimum 30 characters required).'
            }),
            'impact_summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Reputational damage among friends and family'}),
        }

