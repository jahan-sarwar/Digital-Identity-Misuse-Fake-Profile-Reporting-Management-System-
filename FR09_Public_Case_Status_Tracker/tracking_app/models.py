# Data models for Citizen Public Case Tracking
from django.db import models

class TrackableCase(models.Model):
    # Milestone progression stages
    PROGRESS_STAGE_CHOICES = [
        ('1_SUBMITTED', '1. Complaint Registered'),
        ('2_VERIFIED', '2. Complainant Identity Authenticated'),
        ('3_ASSIGNED', '3. Allocated to Forensic Investigator'),
        ('4_INVESTIGATION', '4. Forensic Examination & Platform Takedown Active'),
        ('5_RESOLVED', '5. Offending Profile Neutralized & Case Resolved'),
    ]

    # Unique Case ID and Secure PIN
    case_id = models.CharField(max_length=32, unique=True, help_text="Public Case Reference ID")
    security_pin = models.CharField(max_length=6, default='123456', help_text="6-digit verification PIN provided to citizen")
    
    # Complainant credentials
    complainant_name = models.CharField(max_length=150)
    complainant_email = models.EmailField()
    
    # Incident summary
    platform_name = models.CharField(max_length=50, default='Facebook')
    impersonated_account_name = models.CharField(max_length=150)
    
    # Tracking status
    progress_stage = models.CharField(max_length=30, choices=PROGRESS_STAGE_CHOICES, default='1_SUBMITTED')
    public_status_message = models.CharField(
        max_length=255,
        default='Your complaint has been logged and is awaiting document triage.',
        help_text="Public-facing explanation displayed to citizen"
    )
    
    # Official investigating agency & officer designation
    assigned_agency = models.CharField(max_length=100, default='National Cyber Crime Investigation Division')
    
    # Important milestone dates
    submission_date = models.DateTimeField(auto_now_add=True)
    last_status_update = models.DateTimeField(auto_now=True)
    estimated_completion_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-submission_date']

    def __str__(self):
        return f"{self.case_id} - {self.complainant_name} ({self.get_progress_stage_display()})"

    @property
    def percentage_progress(self):
        # Calculate visual progress percentage
        mapping = {
            '1_SUBMITTED': 20,
            '2_VERIFIED': 40,
            '3_ASSIGNED': 60,
            '4_INVESTIGATION': 80,
            '5_RESOLVED': 100,
        }
        return mapping.get(self.progress_stage, 20)
