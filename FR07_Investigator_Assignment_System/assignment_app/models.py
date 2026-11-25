# Data models for Investigator Staff and Case Assignment
from django.db import models

class InvestigatorStaff(models.Model):
    # Forensic specialization options
    SPECIALIZATION_CHOICES = [
        ('SOCIAL_MEDIA_FRAUD', 'Social Media Fraud & Clone Profiles'),
        ('CYBER_EXTORTION', 'Blackmail & Financial Cyber Extortion'),
        ('DEFAMATION_HARASSMENT', 'Online Harassment & Slander'),
        ('CORPORATE_IDENTITY_THEFT', 'Executive Impersonation & Brand Theft'),
    ]

    # Investigator officer identification
    full_name = models.CharField(max_length=120, help_text="Full legal name of the investigator")
    badge_number = models.CharField(max_length=40, unique=True, help_text="Official investigative badge number")
    email = models.EmailField(unique=True, help_text="Official department email")
    phone = models.CharField(max_length=20, blank=True, help_text="Direct desk/mobile contact")
    
    # Official position
    rank_title = models.CharField(max_length=80, default='Cyber Forensic Investigator', help_text="Official rank/designation")
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, default='SOCIAL_MEDIA_FRAUD')
    
    # Operational workload tracking
    active_caseload = models.PositiveIntegerField(default=0, help_text="Number of active cases currently handled")
    max_caseload_capacity = models.PositiveIntegerField(default=5, help_text="Maximum simultaneous active cases")
    is_available = models.BooleanField(default=True, help_text="Available for immediate case allocation")

    def __str__(self):
        return f"{self.full_name} ({self.badge_number}) - Load: {self.active_caseload}/{self.max_caseload_capacity}"


class CaseAssignment(models.Model):
    # Case operational urgency levels
    PRIORITY_CHOICES = [
        ('LOW', 'Low Priority (Standard SLA: 7 Days)'),
        ('MEDIUM', 'Medium Priority (SLA: 72 Hours)'),
        ('HIGH', 'High Priority (SLA: 24 Hours)'),
        ('URGENT', 'Urgent / Emergency Escalation (SLA: 6 Hours)'),
    ]

    # Assignment lifecycle states
    ASSIGNMENT_STATUS_CHOICES = [
        ('UNASSIGNED', 'Unassigned / In Triage Pool'),
        ('ASSIGNED', 'Assigned to Investigator'),
        ('ACCEPTED_BY_OFFICER', 'Accepted by Assigned Officer'),
        ('IN_PROGRESS', 'Active Investigation Underway'),
        ('COMPLETED', 'Investigation Completed & Closed'),
    ]

    # Unique Case Reference identifier
    case_id = models.CharField(max_length=32, unique=True, help_text="Incident Case ID to be assigned")
    title = models.CharField(max_length=200, help_text="Headline / Brief summary of identity misuse")
    platform = models.CharField(max_length=50, default='Facebook', help_text="Target platform of misuse")
    
    # Assignment relationship to investigator
    assigned_investigator = models.ForeignKey(
        InvestigatorStaff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cases',
        help_text="Investigating officer assigned to this case"
    )
    
    # Operational priority and status
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    assignment_status = models.CharField(max_length=30, choices=ASSIGNMENT_STATUS_CHOICES, default='UNASSIGNED')
    
    # Administrative directives and accountability
    assigned_by = models.CharField(max_length=100, default='Admin Controller', help_text="Name/ID of assigning supervisor")
    supervisor_directives = models.TextField(blank=True, help_text="Specific forensic instructions for the investigator")
    
    # Operational timeline
    assigned_at = models.DateTimeField(null=True, blank=True)
    deadline_date = models.DateField(null=True, blank=True, help_text="Target date for case resolution")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        officer = self.assigned_investigator.full_name if self.assigned_investigator else 'Unassigned'
        return f"[{self.case_id}] {self.title} -> {officer} ({self.get_priority_display()})"
