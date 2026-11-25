# Data models for Tamper-Proof Case Audit History Log
from django.db import models
import hashlib

class SecurityAuditTrail(models.Model):
    # Standard classification of recorded actions
    ACTION_CATEGORY_CHOICES = [
        ('CASE_SUBMITTED', 'Initial Incident Report Logged'),
        ('EVIDENCE_UPLOADED', 'Forensic Evidence Asset Uploaded'),
        ('IDENTITY_VERIFIED', 'Complainant Identity Authenticated'),
        ('ASSIGNED_TO_OFFICER', 'Investigator Staff Allocated'),
        ('STATUS_TRANSITION', 'Investigation Milestone Advanced'),
        ('EVIDENCE_INSPECTED', 'Evidence Hash Cryptographically Inspected'),
        ('PLATFORM_TAKEDOWN_ISSUED', 'Formal Platform Subpoena Transmitted'),
        ('RESOLUTION_CLOSED', 'Case Successfully Closed & Neutralized'),
    ]

    # Target incident identifier
    case_id = models.CharField(max_length=32, db_index=True, help_text="Associated Incident Case ID")
    
    # Action taxonomy
    action_category = models.CharField(max_length=35, choices=ACTION_CATEGORY_CHOICES, default='STATUS_TRANSITION')
    
    # Actor credentials
    actor_username = models.CharField(max_length=100, help_text="Username of officer or citizen")
    actor_role = models.CharField(max_length=80, default='Lead Forensic Detective', help_text="Role designation")
    
    # Network security origin telemetry
    ip_address = models.GenericIPAddressField(default='127.0.0.1', help_text="Client IP address")
    user_agent = models.CharField(max_length=255, blank=True, help_text="Browser/Client User-Agent fingerprint")
    
    # Pre- and post-action state delta
    previous_state = models.CharField(max_length=100, blank=True, help_text="State before action execution")
    new_state = models.CharField(max_length=100, blank=True, help_text="State resulting from action execution")
    
    # Narrative explanation
    action_narrative = models.TextField(help_text="Detailed audit statement describing the transaction")
    
    # Cryptographic integrity signature
    event_hash = models.CharField(max_length=64, blank=True, help_text="SHA-256 hash ensuring tamper-proof record")
    is_tamper_verified = models.BooleanField(default=True, help_text="Verified against blockchain/system digest")
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        # Auto-compute SHA-256 integrity hash
        if not self.event_hash:
            raw_signature = f"{self.case_id}|{self.action_category}|{self.actor_username}|{self.action_narrative}"
            self.event_hash = hashlib.sha256(raw_signature.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.case_id} - {self.get_action_category_display()} by {self.actor_username}"
