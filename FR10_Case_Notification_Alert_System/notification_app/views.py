# Views handling case event notifications and broadcast logs
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CaseEventNotification
from .forms import DispatchNotificationForm

def populate_seed_notifications():
    # Helper to generate seed event alerts if none exist
    if not CaseEventNotification.objects.exists():
        CaseEventNotification.objects.create(
            case_id='CASE-2026-6601',
            recipient_name='Sarwar Jahan',
            recipient_email='sarwar.jahan@example.com',
            recipient_phone='+880 1718-000014',
            event_type='CASE_SUBMITTED',
            notification_channel='EMAIL',
            subject='Acknowledgment: Your Incident Complaint Has Been Registered [CASE-2026-6601]',
            message_body='Dear Sarwar Jahan, your fake-profile report on Facebook has been received and queued for initial forensic review. Your Security PIN is 123456.',
            delivery_status='DELIVERED',
            is_read=True
        )
        CaseEventNotification.objects.create(
            case_id='CASE-2026-6601',
            recipient_name='Sarwar Jahan',
            recipient_email='sarwar.jahan@example.com',
            recipient_phone='+880 1718-000014',
            event_type='INVESTIGATOR_ASSIGNED',
            notification_channel='SMS',
            subject='Case Update: Detective Allocated',
            message_body='CID Alert: Inspector Sarwar Jahan (Badge CID-CYBER-014) has been assigned to lead investigation for case CASE-2026-6601.',
            delivery_status='DELIVERED',
            is_read=False
        )
        CaseEventNotification.objects.create(
            case_id='CASE-2026-6601',
            recipient_name='Sarwar Jahan',
            recipient_email='sarwar.jahan@example.com',
            recipient_phone='+880 1718-000014',
            event_type='TAKEDOWN_REQUESTED',
            notification_channel='IN_APP',
            subject='Legal Takedown Escalated to Meta Legal Operations',
            message_body='A formal removal subpoena has been transmitted to Facebook Trust & Safety under emergency cyber provisions.',
            delivery_status='DELIVERED',
            is_read=False
        )


def notification_inbox_view(request):
    # Ensure seed notifications are loaded
    populate_seed_notifications()

    notifications = CaseEventNotification.objects.all()

    # Filter by channel or unread status
    channel_filter = request.GET.get('channel')
    unread_only = request.GET.get('unread')

    if channel_filter:
        notifications = notifications.filter(notification_channel=channel_filter)
    if unread_only == '1':
        notifications = notifications.filter(is_read=False)

    # Counter metrics
    total_count = CaseEventNotification.objects.count()
    unread_count = CaseEventNotification.objects.filter(is_read=False).count()
    delivered_count = CaseEventNotification.objects.filter(delivery_status='DELIVERED').count()

    context = {
        'notifications': notifications,
        'total_count': total_count,
        'unread_count': unread_count,
        'delivered_count': delivered_count,
        'selected_channel': channel_filter or 'ALL',
        'unread_only': unread_only == '1',
    }
    return render(request, 'notification_app/notification_inbox.html', context)


def mark_notification_read_view(request, notif_id):
    # Mark specific notification as read
    notif = get_object_or_404(CaseEventNotification, id=notif_id)
    notif.is_read = True
    notif.save()
    messages.success(request, f"Notification #{notif.id} marked as read.")
    return redirect('notification_inbox')


def dispatch_notification_view(request):
    # Administrative view to trigger/broadcast an alert
    if request.method == 'POST':
        form = DispatchNotificationForm(request.POST)
        if form.is_valid():
            notif = form.save()
            messages.success(
                request,
                f"Notification dispatched successfully to {notif.recipient_name} ({notif.recipient_email}) via {notif.notification_channel}."
            )
            return redirect('notification_inbox')
    else:
        form = DispatchNotificationForm()

    return render(request, 'notification_app/dispatch_notification.html', {'form': form})
