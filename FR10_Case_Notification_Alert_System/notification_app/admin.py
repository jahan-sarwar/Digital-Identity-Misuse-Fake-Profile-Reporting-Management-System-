# Django admin registration for notification models
from django.contrib import admin
from .models import CaseEventNotification

@admin.register(CaseEventNotification)
class CaseEventNotificationAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'recipient_name', 'event_type', 'notification_channel', 'delivery_status', 'is_read', 'dispatched_at')
    list_filter = ('event_type', 'notification_channel', 'delivery_status', 'is_read')
    search_fields = ('case_id', 'recipient_name', 'recipient_email', 'subject')
