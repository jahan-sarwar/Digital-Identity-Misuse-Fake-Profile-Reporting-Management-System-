# Admin site registration for audit trail
from django.contrib import admin
from .models import SecurityAuditTrail

@admin.register(SecurityAuditTrail)
class SecurityAuditTrailAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'action_category', 'actor_username', 'actor_role', 'ip_address', 'is_tamper_verified', 'timestamp')
    list_filter = ('action_category', 'actor_role', 'is_tamper_verified', 'timestamp')
    search_fields = ('case_id', 'actor_username', 'action_narrative', 'event_hash')
    readonly_fields = ('timestamp', 'event_hash')
