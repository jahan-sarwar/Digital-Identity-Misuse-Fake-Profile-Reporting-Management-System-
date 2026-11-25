# Admin site registration for Investigator Assignment
from django.contrib import admin
from .models import InvestigatorStaff, CaseAssignment

@admin.register(InvestigatorStaff)
class InvestigatorStaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'badge_number', 'rank_title', 'active_caseload', 'max_caseload_capacity', 'is_available')
    list_filter = ('rank_title', 'is_available', 'specialization')
    search_fields = ('full_name', 'badge_number', 'email')

@admin.register(CaseAssignment)
class CaseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'title', 'assigned_investigator', 'priority', 'assignment_status', 'assigned_at')
    list_filter = ('assignment_status', 'priority', 'platform')
    search_fields = ('case_id', 'title', 'assigned_by')
