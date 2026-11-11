import uuid
from django.db import models
from django.core.validators import MinLengthValidator

class IncidentReport(models.Model):
    """
    FR-02: Model capturing incident classification, dates, title, narrative description,
    and impact summary with automatic unique tracking code generation.
    """
    INCIDENT_TYPE_CHOICES = (
        ('FAKE_PROFILE', 'Fake / Impersonation Profile'),
        ('IDENTITY_THEFT', 'Direct Identity Theft & Fraud'),
        ('DEFAMATION', 'Defamatory / Slanderous Content'),
        ('UNAUTHORIZED_MEDIA', 'Unauthorized Photo/Video Usage'),
        ('CYBER_BULLYING', 'Harassment or Cyberbullying'),
        ('OTHER', 'Other Misuse'),
    )

    STATUS_CHOICES = (
        ('SUBMITTED', 'Submitted / Pending Review'),
        ('UNDER_INVESTIGATION', 'Under Investigation'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    )

    case_id = models.CharField(max_length=32, unique=True, editable=False)
    reporter_name = models.CharField(max_length=150, help_text="Complainant Name")
    reporter_email = models.EmailField(help_text="Notification Email")
    incident_type = models.CharField(max_length=30, choices=INCIDENT_TYPE_CHOICES, default='FAKE_PROFILE')
    title = models.CharField(max_length=200, help_text="Short Headline / Summary")
    incident_description = models.TextField(
        validators=[MinLengthValidator(30, message="Incident description must contain at least 30 characters.")],
        help_text="Comprehensive narrative detailing how the identity was misused."
    )
    date_noticed = models.DateField(help_text="Date when misuse was first identified")
    impact_summary = models.CharField(max_length=255, blank=True, null=True, help_text="Financial, reputational, or social impact")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='SUBMITTED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.case_id:
            self.case_id = f"DIM-2026-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.case_id}] {self.title}"

