# Django Admin site registration for unified models
from django.contrib import admin
from .models import (
    UserProfile, IncidentCase, EvidenceFile, IdentityVerification,
    InvestigationNoteEntry, CaseEventNotification, SecurityAuditTrail
)

admin.site.register(UserProfile)
admin.site.register(IncidentCase)
admin.site.register(EvidenceFile)
admin.site.register(IdentityVerification)
admin.site.register(InvestigationNoteEntry)
admin.site.register(CaseEventNotification)
admin.site.register(SecurityAuditTrail)
