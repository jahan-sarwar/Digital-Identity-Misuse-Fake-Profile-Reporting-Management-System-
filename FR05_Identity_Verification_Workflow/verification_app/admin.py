# Django admin panel registration
from django.contrib import admin
from .models import IdentityVerification

@admin.register(IdentityVerification)
class IdentityVerificationAdmin(admin.ModelAdmin):
    # Columns shown in admin list
    list_display = ('case_id', 'reporter_full_name', 'document_type', 'verification_status', 'submitted_at')
    # Filter options
    list_filter = ('verification_status', 'document_type', 'submitted_at')
    # Searchable attributes
    search_fields = ('case_id', 'reporter_full_name', 'reporter_email', 'id_number')
    # Read-only verification token
    readonly_fields = ('verification_token', 'submitted_at', 'reviewed_at')
