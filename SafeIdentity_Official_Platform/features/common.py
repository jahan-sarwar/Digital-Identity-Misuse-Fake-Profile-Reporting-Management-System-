# Shared helper utilities used across all modular feature packages
from portal_app.models import CaseEventNotification, SecurityAuditTrail


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def log_audit_event(request, case_obj, category, prev_state, new_state, narrative):
    # Append a tamper-evident SHA-256 audit log entry
    actor = request.user.username if request.user.is_authenticated else 'anonymous'
    role = (
        request.user.profile.get_role_display()
        if request.user.is_authenticated and hasattr(request.user, 'profile')
        else 'Citizen'
    )
    SecurityAuditTrail.objects.create(
        case=case_obj,
        case_ref=case_obj.case_id if case_obj else 'SYSTEM',
        action_category=category,
        actor_username=actor,
        actor_role=role,
        ip_address=get_client_ip(request),
        previous_state=prev_state,
        new_state=new_state,
        action_narrative=narrative,
    )


def send_case_notification(case_obj, recipient_user, email, channel, subject, body):
    # Dispatch an in-app, email, or SMS notification record
    CaseEventNotification.objects.create(
        case=case_obj,
        recipient=recipient_user,
        recipient_email=email,
        channel=channel,
        subject=subject,
        message_body=body,
    )
