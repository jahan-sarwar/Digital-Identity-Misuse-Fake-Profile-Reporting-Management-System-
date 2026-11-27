# Unified relational database schema combining all reporting, verification, investigation, tracking, notification, audit, and governance features
import uuid
import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import validate_evidence_file


class UserProfile(models.Model):
    # Role-based access control definitions and account governance metadata
    ROLE_CHOICES = [
        ('CITIZEN', 'Citizen / Complainant'),
        ('INVESTIGATOR', 'Forensic Investigator / Support Staff'),
        ('ADMIN', 'System Administrator'),
    ]

    APPROVAL_STATUS_CHOICES = [
        ('PENDING_APPROVAL', 'Pending Administrative Approval'),
        ('APPROVED', 'Approved & Active'),
        ('SUSPENDED', 'Suspended'),
        ('REJECTED', 'Rejected'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    phone_number = models.CharField(max_length=20, blank=True)
    nid_or_passport = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Gatekeeper flags enforcing admin approval before login
    is_approved = models.BooleanField(default=False, db_index=True)
    approval_status = models.CharField(max_length=25, choices=APPROVAL_STATUS_CHOICES, default='PENDING_APPROVAL')
    approval_notes = models.TextField(blank=True)
    approved_by = models.CharField(max_length=100, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    # Investigator roster metadata
    badge_number = models.CharField(max_length=40, blank=True)
    specialization = models.CharField(max_length=100, blank=True, default='Social Media Fraud & Impersonation')
    max_caseload = models.PositiveIntegerField(default=5)
    is_identity_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def active_caseload(self):
        return self.user.assigned_cases.exclude(current_status__in=['RESOLVED', 'REJECTED']).count()

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()}) - {self.approval_status}"


@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, created, **kwargs):
    # Automatically attach a profile whenever a Django User is created
    if created:
        is_super = instance.is_superuser
        UserProfile.objects.create(
            user=instance,
            role='ADMIN' if is_super else 'CITIZEN',
            is_approved=is_super,
            approval_status='APPROVED' if is_super else 'PENDING_APPROVAL',
        )
    elif hasattr(instance, 'profile'):
        instance.profile.save()


class IncidentCase(models.Model):
    # Central case entity connecting reporting, platform URLs, review, assignment, investigation, and public tracking
    PLATFORM_CHOICES = [
        ('FACEBOOK', 'Facebook'),
        ('INSTAGRAM', 'Instagram'),
        ('TWITTER', 'Twitter / X'),
        ('TIKTOK', 'TikTok'),
        ('LINKEDIN', 'LinkedIn'),
        ('YOUTUBE', 'YouTube'),
        ('TELEGRAM', 'Telegram'),
        ('WHATSAPP', 'WhatsApp'),
        ('OTHER', 'Other Social Platform'),
    ]

    INCIDENT_TYPE_CHOICES = [
        ('FAKE_PROFILE', 'Fake / Impersonation Profile'),
        ('IDENTITY_THEFT', 'Direct Identity Theft & Fraud'),
        ('DEFAMATION', 'Defamatory / Slanderous Content'),
        ('UNAUTHORIZED_MEDIA', 'Unauthorized Photo/Video Usage'),
        ('CYBER_BULLYING', 'Harassment or Cyberbullying'),
        ('OTHER', 'Other Misuse'),
    ]

    RISK_LEVEL_CHOICES = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('CRITICAL', 'Critical Risk'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low (7 Days SLA)'),
        ('MEDIUM', 'Medium (72 Hours SLA)'),
        ('HIGH', 'High (24 Hours SLA)'),
        ('URGENT', 'Urgent (6 Hours SLA)'),
    ]

    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted / Pending Review'),
        ('IDENTITY_VERIFIED', 'Identity Verified'),
        ('EVIDENCE_ACCEPTED', 'Evidence Validated'),
        ('ASSIGNED', 'Assigned to Investigator'),
        ('IN_PROGRESS', 'Forensic Analysis In Progress'),
        ('LEGAL_NOTICE_SENT', 'Platform Takedown Issued'),
        ('RESOLVED', 'Neutralized & Resolved'),
        ('REJECTED', 'Rejected / Closed'),
    ]

    # Unique Case ID & 6-digit Security PIN for public tracking
    case_id = models.CharField(max_length=32, unique=True, editable=False, db_index=True)
    security_pin = models.CharField(max_length=6, default='123456')

    # Reporter details
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_cases')
    reporter_name = models.CharField(max_length=150)
    reporter_email = models.EmailField()

    # Platform & target profile details
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='FACEBOOK')
    other_platform_name = models.CharField(max_length=100, blank=True, null=True)
    target_profile_url = models.URLField(max_length=500)
    target_username_or_handle = models.CharField(max_length=100, blank=True, null=True)

    # Incident narrative
    incident_type = models.CharField(max_length=30, choices=INCIDENT_TYPE_CHOICES, default='FAKE_PROFILE')
    title = models.CharField(max_length=200)
    incident_description = models.TextField(
        validators=[MinLengthValidator(30, message="Incident description must contain at least 30 characters.")]
    )
    date_noticed = models.DateField()
    impact_summary = models.CharField(max_length=255, blank=True, null=True)

    # Administrative triage & evidence review
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='MEDIUM')
    reviewer_notes = models.TextField(blank=True)
    reviewed_by = models.CharField(max_length=100, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    # Investigator assignment
    assigned_investigator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cases'
    )
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    deadline_date = models.DateField(null=True, blank=True)
    supervisor_directives = models.TextField(blank=True)
    assigned_at = models.DateTimeField(null=True, blank=True)

    # Active investigation & public status
    current_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='SUBMITTED', db_index=True)
    suspect_lead_info = models.TextField(blank=True)
    platform_takedown_requested = models.BooleanField(default=False)
    platform_ticket_id = models.CharField(max_length=100, blank=True)
    public_status_message = models.CharField(
        max_length=255,
        default='Your complaint has been registered and is queued for administrative review.'
    )
    estimated_completion_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.case_id:
            self.case_id = f"DIM-2026-{uuid.uuid4().hex[:6].upper()}"
        if not self.security_pin:
            self.security_pin = str(uuid.uuid4().int)[:6]
        super().save(*args, **kwargs)

    @property
    def percentage_progress(self):
        mapping = {
            'SUBMITTED': 15,
            'IDENTITY_VERIFIED': 30,
            'EVIDENCE_ACCEPTED': 45,
            'ASSIGNED': 60,
            'IN_PROGRESS': 75,
            'LEGAL_NOTICE_SENT': 90,
            'RESOLVED': 100,
            'REJECTED': 100,
        }
        return mapping.get(self.current_status, 15)

    def __str__(self):
        return f"[{self.case_id}] {self.title}"


class EvidenceFile(models.Model):
    # Supporting screenshots and PDF documents attached to an incident case
    FILE_TYPE_CHOICES = [
        ('SCREENSHOT', 'Profile Screenshot'),
        ('CHAT_LOG', 'Chat / Message Log'),
        ('ID_COMPARISON', 'Real vs Fake Comparison'),
        ('DOCUMENT', 'Supporting Document / PDF'),
    ]

    case = models.ForeignKey(IncidentCase, on_delete=models.CASCADE, related_name='evidences')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='evidence/%Y/%m/', validators=[validate_evidence_file])
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='SCREENSHOT')
    caption = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(editable=False, default=0)
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
        return f"{self.case.case_id} - {self.get_file_type_display()}"


class IdentityVerification(models.Model):
    # Complainant identity authentication documents linked to a case
    DOCUMENT_CHOICES = [
        ('NID', 'National Identification Card (NID)'),
        ('PASSPORT', 'International Passport'),
        ('DRIVING_LICENSE', 'Driving License'),
        ('STUDENT_ID', 'Institutional / Student ID Card'),
        ('OFFICIAL_BADGE', 'Government or Corporate Badge'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Verification'),
        ('VERIFIED', 'Officially Verified'),
        ('REJECTED', 'Rejected / Discrepancy Found'),
    ]

    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    case = models.ForeignKey(IncidentCase, on_delete=models.CASCADE, related_name='verifications')
    reporter_full_name = models.CharField(max_length=150)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_CHOICES, default='NID')
    id_number = models.CharField(max_length=50)
    document_file = models.FileField(upload_to='identity_docs/%Y/%m/', validators=[validate_evidence_file])
    selfie_photo = models.ImageField(upload_to='identity_selfies/%Y/%m/')
    verification_status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True)
    rejection_reason = models.CharField(max_length=255, blank=True)
    reviewed_by = models.CharField(max_length=100, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.case.case_id} - {self.reporter_full_name} ({self.verification_status})"


class InvestigationNoteEntry(models.Model):
    # Chronological forensic investigation journal entries
    NOTE_TYPE_CHOICES = [
        ('STATUS_CHANGE', 'Status Transition'),
        ('FORENSIC_EXAMINATION', 'Digital Forensic / OSINT Finding'),
        ('PLATFORM_CORRESPONDENCE', 'Platform Subpoena / Takedown Log'),
        ('INTERVIEW_DEPOSITION', 'Complainant / Witness Interview'),
        ('INTERNAL_STRATEGY', 'Confidential Investigation Memo'),
    ]

    case = models.ForeignKey(IncidentCase, on_delete=models.CASCADE, related_name='notes')
    officer_name = models.CharField(max_length=100)
    note_type = models.CharField(max_length=30, choices=NOTE_TYPE_CHOICES, default='FORENSIC_EXAMINATION')
    is_confidential = models.BooleanField(default=False)
    previous_status = models.CharField(max_length=40, blank=True)
    new_status = models.CharField(max_length=40, blank=True)
    detailed_notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.case.case_id} - {self.officer_name} ({self.note_type})"


class CaseEventNotification(models.Model):
    # Event-triggered notification alerts across Email, SMS, and In-App Inbox
    CHANNEL_CHOICES = [
        ('IN_APP', 'In-App Notification Inbox'),
        ('EMAIL', 'Email Dispatch'),
        ('SMS', 'SMS Gateway Alert'),
    ]

    case = models.ForeignKey(IncidentCase, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    recipient_email = models.EmailField(blank=True)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='IN_APP')
    subject = models.CharField(max_length=200)
    message_body = models.TextField()
    is_read = models.BooleanField(default=False)
    dispatched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dispatched_at']

    def __str__(self):
        return f"[{self.channel}] {self.subject}"


class SecurityAuditTrail(models.Model):
    # Tamper-evident audit trail recording all system actions with SHA-256 digests
    case = models.ForeignKey(IncidentCase, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    case_ref = models.CharField(max_length=32, db_index=True)
    action_category = models.CharField(max_length=50)
    actor_username = models.CharField(max_length=100)
    actor_role = models.CharField(max_length=60)
    ip_address = models.GenericIPAddressField(default='127.0.0.1')
    previous_state = models.CharField(max_length=100, blank=True)
    new_state = models.CharField(max_length=100, blank=True)
    action_narrative = models.TextField()
    event_hash = models.CharField(max_length=64, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if not self.event_hash:
            raw_sig = f"{self.case_ref}|{self.action_category}|{self.actor_username}|{self.action_narrative}"
            self.event_hash = hashlib.sha256(raw_sig.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.case_ref}] {self.action_category} by {self.actor_username}"
