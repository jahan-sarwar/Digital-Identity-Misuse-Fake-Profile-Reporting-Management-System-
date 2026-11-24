# Django admin registration for tracking models
from django.contrib import admin
from .models import TrackableCase

@admin.register(TrackableCase)
class TrackableCaseAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'complainant_name', 'platform_name', 'progress_stage', 'submission_date', 'last_status_update')
    list_filter = ('progress_stage', 'platform_name')
    search_fields = ('case_id', 'complainant_name', 'complainant_email')
