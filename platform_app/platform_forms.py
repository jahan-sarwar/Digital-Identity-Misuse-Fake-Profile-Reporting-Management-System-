from django import forms
from django.core.exceptions import ValidationError
from .models import PlatformReport
from .url_validators import validate_platform_profile_url

class PlatformSubmissionForm(forms.ModelForm):
    """
    Dedicated Form for selecting social media platform and submitting profile URL.
    Performs cross-field validation to ensure URL matches platform domain.
    """
    class Meta:
        model = PlatformReport
        fields = [
            'reporter_name',
            'platform',
            'other_platform_name',
            'target_profile_url',
            'target_username_or_handle',
        ]
        widgets = {
            'reporter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'other_platform_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specify if Other'}),
            'target_profile_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.facebook.com/fake.profile.123'}),
            'target_username_or_handle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., @fake_victim_2026'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        platform = cleaned_data.get('platform')
        other_platform_name = cleaned_data.get('other_platform_name')
        target_profile_url = cleaned_data.get('target_profile_url')

        if platform == 'OTHER' and not other_platform_name:
            self.add_error('other_platform_name', "Please specify the platform name when 'Other Social Platform' is selected.")

        if platform and target_profile_url:
            try:
                validate_platform_profile_url(platform, target_profile_url)
            except ValidationError as exc:
                self.add_error('target_profile_url', exc.message)

        return cleaned_data

