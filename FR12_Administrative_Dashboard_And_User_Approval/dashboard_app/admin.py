# Django admin registration
from django.contrib import admin
from .models import SystemUserAccount, AdministrativeCaseMetric

@admin.register(SystemUserAccount)
class SystemUserAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'assigned_role', 'is_approved', 'approval_status', 'registered_at')
    list_filter = ('is_approved', 'approval_status', 'assigned_role')
    search_fields = ('username', 'full_name', 'email', 'department')
    readonly_fields = ('registered_at', 'approved_at')

@admin.register(AdministrativeCaseMetric)
class AdministrativeCaseMetricAdmin(admin.ModelAdmin):
    list_display = ('metric_title', 'metric_value', 'category', 'updated_at')
