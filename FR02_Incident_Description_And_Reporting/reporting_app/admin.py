from django.contrib import admin
from .models import IncidentReport

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'reporter_name', 'incident_type', 'title', 'status', 'created_at')
    list_filter = ('incident_type', 'status', 'created_at')
    search_fields = ('case_id', 'reporter_name', 'title', 'incident_description')
    readonly_fields = ('case_id', 'created_at', 'updated_at')

