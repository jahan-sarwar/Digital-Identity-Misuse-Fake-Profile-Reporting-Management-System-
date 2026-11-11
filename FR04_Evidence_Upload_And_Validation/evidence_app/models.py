import uuid
from django.db import models
from .file_validators import validate_evidence_file

class EvidenceFile(models.Model):
    """
    FR-04: Model representing an uploaded supporting evidence document or image.
    Stores file binary, calculated file size in bytes, descriptive caption, and timestamp.
    """
    FILE_TYPE_CHOICES = (
        ('SCREENSHOT', 'Profile Screenshot'),
        ('CHAT_LOG', 'Chat / Message Log'),
        ('ID_COMPARISON', 'Real vs Fake Comparison'),
        ('DOCUMENT', 'Supporting Document / PDF'),
    )

    case_id = models.CharField(max_length=32, help_text="Associated Incident Case ID")
    uploader_name = models.CharField(max_length=150, help_text="Complainant Name")
    file = models.FileField(
        upload_to='evidence/%Y/%m/',
        validators=[validate_evidence_file],
        help_text="Allowed formats: JPG, JPEG, PNG, PDF (Max 5MB)"
    )
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='SCREENSHOT')
    caption = models.CharField(max_length=255, blank=True, help_text="What does this evidence show?")
    file_size = models.PositiveIntegerField(editable=False, default=0, help_text="Size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        if self.file and hasattr(self.file, 'size'):
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    def is_pdf(self):
        return self.file.name.lower().endswith('.pdf')

    def __str__(self):
        return f"[{self.case_id}] {self.get_file_type_display()} - {self.caption or self.file.name}"

