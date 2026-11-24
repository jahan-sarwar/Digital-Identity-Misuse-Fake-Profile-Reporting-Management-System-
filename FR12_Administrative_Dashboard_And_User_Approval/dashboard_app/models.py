# Data models for User Account Approval and Administrative Statistics
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class SystemUserAccount(models.Model):
    # System authorization roles
    ROLE_CHOICES = [
        ('CITIZEN_REPORTER', 'Citizen / Complainant Reporter'),
        ('FORENSIC_INVESTIGATOR', 'CID Cyber Forensic Investigator'),
        ('TRIAGE_SUPERVISOR', 'Triage & Case Review Supervisor'),
        ('SYSTEM_ADMINISTRATOR', 'Security System Administrator'),
    ]

    # Administrative approval workflow states
    APPROVAL_STATUS_CHOICES = [
        ('PENDING_APPROVAL', 'Pending Security Administrator Approval'),
        ('APPROVED', 'Account Officially Approved & Active'),
        ('SUSPENDED', 'Account Temporarily Suspended'),
        ('REJECTED', 'Registration Application Rejected'),
    ]

    # Identity credentials
    username = models.CharField(max_length=100, unique=True, help_text="Unique system login username")
    full_name = models.CharField(max_length=150, help_text="Legal full name of user")
    email = models.EmailField(unique=True, help_text="Official email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact telephone/mobile")
    password_hash = models.CharField(max_length=128, help_text="Cryptographically hashed password")
    
    # Role assignment and organizational department
    assigned_role = models.CharField(max_length=35, choices=ROLE_CHOICES, default='CITIZEN_REPORTER')
    department = models.CharField(max_length=100, default='General Public / External', blank=True)
    
    # Crucial administrative gatekeeper approval flag
    is_approved = models.BooleanField(default=False, help_text="Access blocked unless approved by Admin")
    approval_status = models.CharField(max_length=25, choices=APPROVAL_STATUS_CHOICES, default='PENDING_APPROVAL')
    
    # Admin approval review metadata
    admin_approval_notes = models.TextField(blank=True, help_text="Remarks by approving security administrator")
    approved_by = models.CharField(max_length=100, blank=True, help_text="Name of reviewing admin")
    
    # Audit timestamps
    registered_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-registered_at']

    def set_password(self, raw_password):
        # Hash user password using secure PBKDF2 algorithm
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        # Validate raw password against stored cryptographic hash
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        approval = "APPROVED" if self.is_approved else "PENDING"
        return f"{self.username} ({self.full_name}) - [{self.assigned_role}] - {approval}"


class AdministrativeCaseMetric(models.Model):
    # Executive dashboard summary metrics
    metric_title = models.CharField(max_length=100)
    metric_value = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, default='SYSTEM')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.metric_title}: {self.metric_value}"
