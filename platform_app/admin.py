from django.contrib import admin
from .models import PlatformReport

@admin.register(PlatformReport)
class PlatformReportAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'reporter_name', 'platform', 'target_username_or_handle', 'created_at')
    list_filter = ('platform', 'created_at')
    search_fields = ('case_id', 'reporter_name', 'target_profile_url', 'target_username_or_handle')
    readonly_fields = ('case_id', 'created_at')

