# Data models for Case Status Updates and Forensic Investigation Notes
from django.db import models

class InvestigationCase(models.Model):
    # Investigation progression milestones
    STATUS_CHOICES = [
        ('ASSIGNED', 'Assigned - Initial Briefing'),
        ('IN_PROGRESS', 'Forensic Analysis In Progress'),
        ('EVIDENCE_VERIFIED', 'Digital Evidence Confirmed'),
        ('LEGAL_NOTICE_SENT', 'Platform Legal Takedown Notice Issued'),
        ('ESCALATED_TO_PLATFORM', 'Escalated to Global Trust & Safety Desk'),
        ('RESOLVED', 'Offending Profile Neutralized / Resolved'),
        ('CLOSED_UNRESOLVED', 'Case Closed / Inconclusive Evidence'),
    ]

    # Unique Case Reference code
    case_id = models.CharField(max_length=32, unique=True, help_text="Unique Case Reference Number")
    case_title = models.CharField(max_length=200, help_text="Subject title of the complaint")
    victim_name = models.CharField(max_length=150, help_text="Complainant legal name")
    
    # Designated investigating detective
    investigating_officer = models.CharField(max_length=100, default='Inspector Sarwar', help_text="Assigned Officer Name")
    
    # Current active workflow status
    current_status = models.CharField(max_length=35, choices=STATUS_CHOICES, default='IN_PROGRESS')
    
    # Investigative leads and suspect dossier
    suspect_lead_info = models.TextField(blank=True, help_text="Forensic details: ISP, IP logs, suspected handle aliases")
    
    # Platform takedown request status
    platform_takedown_requested = models.BooleanField(default=False, help_text="Formal takedown ticket submitted")
    platform_ticket_id = models.CharField(max_length=100, blank=True, help_text="Platform legal case ticket ID")
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.case_id} - {self.case_title} [{self.get_current_status_display()}]"


class InvestigationNoteEntry(models.Model):
    # Classification of investigation notes
    NOTE_TYPE_CHOICES = [
        ('STATUS_CHANGE', 'Status Transition & Operational Event'),
        ('FORENSIC_EXAMINATION', 'Digital Forensic / OSINT Finding'),
        ('PLATFORM_CORRESPONDENCE', 'Platform Communication / Subpoena Response'),
        ('INTERVIEW_DEPOSITION', 'Complainant or Witness Interview Note'),
        ('INTERNAL_STRATEGY', 'Confidential Legal Strategy Memo'),
    ]

    # Relation to parent investigation case
    case = models.ForeignKey(
        InvestigationCase,
        on_delete=models.CASCADE,
        related_name='investigation_notes',
        help_text="Investigation case record"
    )
    
    # Author officer signature
    officer_name = models.CharField(max_length=100, help_text="Name of logging investigator")
    
    # Classification and confidentiality
    note_type = models.CharField(max_length=30, choices=NOTE_TYPE_CHOICES, default='FORENSIC_EXAMINATION')
    is_confidential = models.BooleanField(default=False, help_text="Restricted to senior forensic officers")
    
    # Status progression snapshot
    previous_status = models.CharField(max_length=40, blank=True)
    new_status = models.CharField(max_length=40, blank=True)
    
    # Detailed case note body
    detailed_notes = models.TextField(help_text="Comprehensive investigative findings and observations")
    
    # Entry timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note by {self.officer_name} on {self.case.case_id} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
