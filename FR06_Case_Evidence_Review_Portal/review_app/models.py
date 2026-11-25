# Models for Case & Evidence Review System
from django.db import models

class IncidentReviewCase(models.Model):
    # Assessment priority levels
    RISK_LEVEL_CHOICES = [
        ('LOW', 'Low Risk - Minor Misuse'),
        ('MEDIUM', 'Medium Risk - Impersonation Detected'),
        ('HIGH', 'High Risk - Financial / Reputational Extortion'),
        ('CRITICAL', 'Critical Risk - Severe Defamation / Identity Fraud'),
    ]

    # Administrative triage stages
    REVIEW_STATUS_CHOICES = [
        ('PENDING_TRIAGE', 'Pending Administrative Triage'),
        ('EVIDENCE_ACCEPTED', 'Evidence Validated & Accepted'),
        ('EVIDENCE_INSUFFICIENT', 'Insufficient Supporting Evidence'),
        ('UNDER_INVESTIGATION', 'Transferred to Forensics / Investigation'),
        ('DISMISSED', 'Dismissed / Ineligible Claim'),
    ]

    # Target social network platforms
    PLATFORM_CHOICES = [
        ('FACEBOOK', 'Facebook'),
        ('INSTAGRAM', 'Instagram'),
        ('LINKEDIN', 'LinkedIn'),
        ('TWITTER_X', 'X (Twitter)'),
        ('TIKTOK', 'TikTok'),
        ('WHATSAPP', 'WhatsApp / Telegram'),
        ('OTHER', 'Other Platform'),
    ]

    # Unique Case Reference identifier
    case_id = models.CharField(max_length=32, unique=True, help_text="Unique Case Reference Number")
    
    # Complainant information
    complainant_name = models.CharField(max_length=150, help_text="Name of reporting citizen")
    complainant_email = models.EmailField(help_text="Notification email address")
    
    # Offending profile details
    target_platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES, default='FACEBOOK')
    fake_profile_url = models.URLField(max_length=300, help_text="Direct URL to reported fake profile")
    impersonated_name = models.CharField(max_length=150, help_text="Name displayed on the fraudulent account")
    
    # Incident narrative description
    incident_narrative = models.TextField(help_text="Full statement detailing the misuse incident")
    
    # Triage and risk scoring
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='MEDIUM')
    review_status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='PENDING_TRIAGE')
    
    # Attached evidence inventory count
    evidence_count = models.PositiveIntegerField(default=1, help_text="Number of supporting files uploaded")
    evidence_summary = models.CharField(max_length=255, blank=True, help_text="Summary of uploaded evidence types")
    
    # Administrative findings and remarks
    reviewer_notes = models.TextField(blank=True, help_text="Internal notes by review officer")
    reviewed_by = models.CharField(max_length=100, blank=True, help_text="Username of triage administrator")
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"[{self.case_id}] {self.complainant_name} vs {self.impersonated_name} ({self.get_review_status_display()})"
