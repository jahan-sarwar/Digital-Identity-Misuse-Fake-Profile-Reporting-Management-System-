# Unified Django forms covering authentication, reporting, verification, review, assignment, and governance
from django import forms
from django.contrib.auth.models import User
from .models import (
    UserProfile, IncidentCase, EvidenceFile, IdentityVerification,
    InvestigationNoteEntry, CaseEventNotification
)


class RegistrationForm(forms.ModelForm):
    # User account registration form with role selection and password confirmation
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your legal full name'})
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+880 1XXXXXXXXX'})
    )
    requested_role = forms.ChoiceField(
        choices=[
            ('CITIZEN', 'Citizen / Complainant'),
            ('INVESTIGATOR', 'Forensic Investigator / Support Staff'),
            ('ADMIN', 'System Administrator'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Minimum 8 characters'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a unique username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned


class LoginForm(forms.Form):
    # Login form supporting username or email
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class ProfileUpdateForm(forms.ModelForm):
    # Account profile management form
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'nid_or_passport', 'gender', 'date_of_birth', 'address', 'avatar']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'nid_or_passport': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class IncidentSubmissionForm(forms.ModelForm):
    # Unified complaint submission form capturing platform, URL, incident type, narrative, and impact
    class Meta:
        model = IncidentCase
        fields = [
            'reporter_name', 'reporter_email', 'platform', 'other_platform_name',
            'target_profile_url', 'target_username_or_handle', 'incident_type',
            'title', 'incident_description', 'date_noticed', 'impact_summary'
        ]
        widgets = {
            'reporter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'reporter_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Notification email'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'other_platform_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specify if Other'}),
            'target_profile_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/fake.profile'}),
            'target_username_or_handle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@fake_handle'}),
            'incident_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief headline of the incident'}),
            'incident_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the identity misuse in detail (minimum 30 characters)...'}),
            'date_noticed': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'impact_summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Financial, reputational, or personal impact'}),
        }


class EvidenceUploadForm(forms.ModelForm):
    # Supporting evidence upload form
    class Meta:
        model = EvidenceFile
        fields = ['file', 'file_type', 'caption']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
            'file_type': forms.Select(attrs={'class': 'form-select'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Describe what this evidence demonstrates'}),
        }


class IdentityVerificationForm(forms.ModelForm):
    # Complainant identity verification submission form
    class Meta:
        model = IdentityVerification
        fields = ['reporter_full_name', 'document_type', 'id_number', 'document_file', 'selfie_photo']
        widgets = {
            'reporter_full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Legal full name on ID'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document serial / NID number'}),
            'document_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
            'selfie_photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class CaseTriageReviewForm(forms.ModelForm):
    # Administrator evidence triage and risk assessment form
    class Meta:
        model = IncidentCase
        fields = ['risk_level', 'current_status', 'reviewer_notes', 'public_status_message']
        widgets = {
            'risk_level': forms.Select(attrs={'class': 'form-select'}),
            'current_status': forms.Select(attrs={'class': 'form-select'}),
            'reviewer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Internal triage review findings...'}),
            'public_status_message': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CaseAssignmentForm(forms.ModelForm):
    # Administrator investigator assignment form
    class Meta:
        model = IncidentCase
        fields = ['assigned_investigator', 'priority', 'deadline_date', 'supervisor_directives']
        widgets = {
            'assigned_investigator': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'deadline_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'supervisor_directives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Directives for the investigating officer...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_investigator'].queryset = User.objects.filter(
            profile__role__in=['INVESTIGATOR', 'ADMIN'],
            profile__is_approved=True
        )


class InvestigationProgressForm(forms.ModelForm):
    # Investigator status transition and lead update form
    class Meta:
        model = IncidentCase
        fields = ['current_status', 'suspect_lead_info', 'platform_takedown_requested', 'platform_ticket_id', 'public_status_message', 'estimated_completion_date']
        widgets = {
            'current_status': forms.Select(attrs={'class': 'form-select'}),
            'suspect_lead_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Suspect IP logs, aliases, or forensic leads...'}),
            'platform_takedown_requested': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'platform_ticket_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. META-LEGAL-88291'}),
            'public_status_message': forms.TextInput(attrs={'class': 'form-control'}),
            'estimated_completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class InvestigationNoteForm(forms.ModelForm):
    # Chronological forensic journal note form
    class Meta:
        model = InvestigationNoteEntry
        fields = ['note_type', 'is_confidential', 'detailed_notes']
        widgets = {
            'note_type': forms.Select(attrs={'class': 'form-select'}),
            'is_confidential': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'detailed_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Record forensic observations or correspondence...'}),
        }
