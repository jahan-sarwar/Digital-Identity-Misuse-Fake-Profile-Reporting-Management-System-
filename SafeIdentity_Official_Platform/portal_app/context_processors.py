# Context processor exposing live notification and approval badges across all templates
from .models import CaseEventNotification, UserProfile


def portal_notifications_context(request):
    unread_notifications = CaseEventNotification.objects.filter(is_read=False).count()
    pending_approvals = UserProfile.objects.filter(
        is_approved=False,
        approval_status='PENDING_APPROVAL'
    ).count()
    return {
        'global_unread_notifications': unread_notifications,
        'global_pending_approvals': pending_approvals,
    }
