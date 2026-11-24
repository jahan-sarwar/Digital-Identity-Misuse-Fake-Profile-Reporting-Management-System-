# Django admin site registration
from django.contrib import admin
from .models import InvestigationCase, InvestigationNoteEntry

@admin.register(InvestigationCase)
class InvestigationCaseAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'case_title', 'victim_name', 'investigating_officer', 'current_status', 'updated_at')
    list_filter = ('current_status', 'platform_takedown_requested', 'updated_at')
    search_fields = ('case_id', 'case_title', 'victim_name', 'investigating_officer')

@admin.register(InvestigationNoteEntry)
class InvestigationNoteEntryAdmin(admin.ModelAdmin):
    list_display = ('case', 'officer_name', 'note_type', 'is_confidential', 'created_at')
    list_filter = ('note_type', 'is_confidential', 'created_at')
    search_fields = ('case__case_id', 'officer_name', 'detailed_notes')
