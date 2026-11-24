# Forms for user registration, login, and admin approval actions
from django import forms
from .models import SystemUserAccount

class UserRegistrationForm(forms.ModelForm):
    # Form for new user account registration
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create strong password'}),
        help_text="Minimum 8 characters"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = SystemUserAccount
        fields = ['username', 'full_name', 'email', 'phone', 'assigned_role', 'department']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. sarwar.jahan'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Legal Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+880 1XXXXXXXXX'}),
            'assigned_role': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Cyber Forensics Lab / University'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        cpwd = cleaned_data.get('confirm_password')
        if pwd and cpwd and pwd != cpwd:
            raise forms.ValidationError("Passwords do not match. Please re-enter identical passwords.")
        return cleaned_data


class UserLoginForm(forms.Form):
    # Form for logging in and checking admin approval
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
