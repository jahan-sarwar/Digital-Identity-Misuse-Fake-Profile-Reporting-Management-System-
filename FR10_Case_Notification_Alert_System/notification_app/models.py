# Data models for Case Event Notification and Alert Dispatch
from django.db import models

class CaseEventNotification(models.Model):
    # Lifecycle event triggers that trigger notifications
    EVENT_TYPE_CHOICES = [
        ('CASE_SUBMITTED', 'Incident Report Registration Confirmed'),
        ('EVIDENCE_VERIFIED', 'Identity & Supporting Evidence Verified'),
        ('INVESTIGATOR_ASSIGNED', 'Investigating Officer Allocated'),
        ('TAKEDOWN_REQUESTED', 'Platform Legal Takedown Notice Issued'),
        ('STATUS_UPDATED', 'Milestone Progression Updated'),
        ('CASE_RESOLVED', 'Fraudulent Profile Neutralized / Closed'),
    ]

    # Delivery gateway channels
    CHANNEL_CHOICES = [
        ('EMAIL', 'Official Email Dispatch'),
        ('SMS', 'Emergency SMS Gateway Alert'),
        ('IN_APP', 'Citizen Secure Dashboard Inbox'),
        ('SYSTEM_WEBHOOK', 'Automated Law Enforcement Webhook'),
    ]

    # Message transmission states
    DELIVERY_STATUS_CHOICES = [
        ('QUEUED', 'Queued in Dispatch Buffer'),
        ('SENT', 'Successfully Dispatched'),
        ('DELIVERED', 'Delivered & Acknowledged by Carrier'),
        ('FAILED', 'Transmission Failed / Bounced'),
    ]

    # Associated case identification
    case_id = models.CharField(max_length=32, help_text="Associated Incident Case ID")
    
    # Recipient credentials
    recipient_name = models.CharField(max_length=150, help_text="Complainant or Officer Name")
    recipient_email = models.EmailField(help_text="Destination email address")
    recipient_phone = models.CharField(max_length=20, blank=True, help_text="SMS phone number")
    
    # Trigger classification & medium
    event_type = models.CharField(max_length=35, choices=EVENT_TYPE_CHOICES, default='STATUS_UPDATED')
    notification_channel = models.CharField(max_length=25, choices=CHANNEL_CHOICES, default='EMAIL')
    
    # Message content headers and body
    subject = models.CharField(max_length=200, help_text="Notification alert headline")
    message_body = models.TextField(help_text="Full notification text received by user")
    
    # Transmission telemetry
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='DELIVERED')
    is_read = models.BooleanField(default=False, help_text="Marked as read in citizen inbox")
    
    # Dispatch timestamp
    dispatched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dispatched_at']

    def __str__(self):
        return f"[{self.case_id}] {self.recipient_name} ({self.get_event_type_display()} via {self.notification_channel})"
