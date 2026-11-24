# Forms for dispatching custom notification alerts
from django import forms
from .models import CaseEventNotification

class DispatchNotificationForm(forms.ModelForm):
    # Form to simulate or broadcast real-time alerts
    class Meta:
        model = CaseEventNotification
        fields = [
            'case_id',
            'recipient_name',
            'recipient_email',
            'recipient_phone',
            'event_type',
            'notification_channel',
            'subject',
            'message_body',
        ]
        widgets = {
            'case_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CASE-2026-6601'}),
            'recipient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Citizen / Officer Name'}),
            'recipient_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'citizen@example.com'}),
            'recipient_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+880 1XXXXXXXXX'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'notification_channel': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Important Update Regarding Your Case'}),
            'message_body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter comprehensive update details, verification outcome, or next action steps...'
            }),
        }
