# Data models for Identity Verification Workflow
from django.db import models
import uuid

class IdentityVerification(models.Model):
    # Supported government/official ID types
    DOCUMENT_CHOICES = [
        ('NID', 'National Identification Card (NID)'),
        ('PASSPORT', 'International Passport'),
        ('DRIVING_LICENSE', 'Driving License'),
        ('STUDENT_ID', 'Institutional / Student ID Card'),
        ('OFFICIAL_BADGE', 'Government or Corporate Security Badge'),
    ]

    # Verification workflow stages
    STATUS_CHOICES = [
        ('PENDING', 'Pending Administrative Review'),
        ('UNDER_REVIEW', 'Under Document Forensic Verification'),
        ('VERIFIED', 'Officially Verified & Authenticated'),
        ('REJECTED', 'Verification Rejected / Discrepancy Found'),
    ]

    # Unique tracking code for verification
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Associated incident case identification
    case_id = models.CharField(max_length=32, help_text="Case ID associated with the identity report")
    
    # Complainant personal credentials
    reporter_full_name = models.CharField(max_length=150, help_text="Legal full name of the complainant")
    reporter_email = models.EmailField(help_text="Active email address for verification updates")
    reporter_phone = models.CharField(max_length=20, blank=True, help_text="Contact number for SMS/OTP verification")
    
    # Identification document metadata
    document_type = models.CharField(max_length=30, choices=DOCUMENT_CHOICES, default='NID')
    id_number = models.CharField(max_length=50, help_text="Document serial or registration number")
    
    # Document and selfie uploads
    document_file = models.FileField(upload_to='identity_docs/%Y/%m/', help_text="Scanned copy of official ID card/passport")
    selfie_photo = models.ImageField(upload_to='identity_selfies/%Y/%m/', help_text="Clear selfie photograph holding the case ID")
    
    # Administrative verification outcome
    verification_status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True, help_text="Internal remarks by verification officer")
    rejection_reason = models.CharField(max_length=255, blank=True, help_text="Reason if document verification fails")
    reviewed_by = models.CharField(max_length=100, blank=True, help_text="Name of investigating officer")
    
    # Audit timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Sort newest submissions first
        ordering = ['-submitted_at']

    def __str__(self):
        # Display label for admin and logs
        return f"{self.case_id} - {self.reporter_full_name} ({self.get_verification_status_display()})"
