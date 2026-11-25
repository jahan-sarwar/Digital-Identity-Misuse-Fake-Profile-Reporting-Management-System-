# Django admin panel registration
from django.contrib import admin
from .models import IncidentReviewCase

@admin.register(IncidentReviewCase)
class IncidentReviewCaseAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'complainant_name', 'target_platform', 'risk_level', 'review_status', 'submitted_at')
    list_filter = ('review_status', 'risk_level', 'target_platform', 'submitted_at')
    search_fields = ('case_id', 'complainant_name', 'fake_profile_url', 'impersonated_name')
