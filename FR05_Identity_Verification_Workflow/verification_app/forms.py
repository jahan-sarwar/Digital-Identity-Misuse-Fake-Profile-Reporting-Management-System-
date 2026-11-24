# HTML form definitions with validation
from django import forms
from .models import IdentityVerification

class IdentityVerificationForm(forms.ModelForm):
    # Form initialization and widget styling
    class Meta:
        model = IdentityVerification
        fields = [
            'case_id',
            'reporter_full_name',
            'reporter_email',
            'reporter_phone',
            'document_type',
            'id_number',
            'document_file',
            'selfie_photo',
        ]
        widgets = {
            # Case reference field
            'case_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. CASE-2026-9481',
                'required': 'required'
            }),
            # Complainant name field
            'reporter_full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your legal full name',
                'required': 'required'
            }),
            # Complainant email field
            'reporter_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
                'required': 'required'
            }),
            # Complainant contact phone
            'reporter_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+880 1XXXXXXXXX'
            }),
            # Identity document dropdown
            'document_type': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            # Identity serial number
            'id_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 199826391000123',
                'required': 'required'
            }),
            # Scanned document file
            'document_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.jpg,.jpeg,.png,.pdf',
                'required': 'required'
            }),
            # Selfie photo file
            'selfie_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': 'required'
            }),
        }

    def clean_document_file(self):
        # Validate uploaded document size under 5MB
        uploaded_file = self.cleaned_data.get('document_file')
        if uploaded_file and uploaded_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Document file size must not exceed 5MB.")
        return uploaded_file
