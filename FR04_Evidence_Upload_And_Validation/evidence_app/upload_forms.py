from django import forms
from .models import EvidenceFile
from .file_validators import validate_evidence_file

class SingleEvidenceUploadForm(forms.ModelForm):
    """
    FR-04: Single evidence upload form with metadata.
    """
    class Meta:
        model = EvidenceFile
        fields = ['case_id', 'uploader_name', 'file', 'file_type', 'caption']
        widgets = {
            'case_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., DIM-2026-A1B2C3D4'}),
            'uploader_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'file_type': forms.Select(attrs={'class': 'form-select'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Screenshot showing impersonating bio and profile photo'}),
        }


class MultiEvidenceUploadForm(forms.Form):
    """
    FR-04: Multi-file evidence upload form allowing primary and secondary attachments simultaneously.
    """
    case_id = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., DIM-2026-A1B2C3D4'})
    )
    uploader_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'})
    )
    primary_evidence = forms.FileField(
        validators=[validate_evidence_file],
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text="Primary Evidence (JPG, PNG, PDF - Max 5MB)"
    )
    primary_caption = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Caption for primary evidence'})
    )
    secondary_evidence = forms.FileField(
        required=False,
        validators=[validate_evidence_file],
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text="Secondary Evidence (Optional)"
    )
    secondary_caption = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Caption for secondary evidence'})
    )

