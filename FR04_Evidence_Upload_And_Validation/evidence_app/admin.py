from django.contrib import admin
from .models import EvidenceFile

@admin.register(EvidenceFile)
class EvidenceFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'case_id', 'uploader_name', 'file_type', 'file_size', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('case_id', 'uploader_name', 'caption')
    readonly_fields = ('file_size', 'uploaded_at')

