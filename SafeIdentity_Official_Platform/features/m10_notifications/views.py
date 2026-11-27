# Module 10: Automated Notification Inbox & Alert Management
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from portal_app.models import CaseEventNotification


@login_required
def notifications_view(request):
    # List notifications relevant to the logged-in user role
    if request.user.profile.role in ['ADMIN', 'INVESTIGATOR']:
        alerts = CaseEventNotification.objects.all()
    else:
        alerts = CaseEventNotification.objects.filter(
            Q(recipient=request.user) | Q(recipient_email=request.user.email)
        )

    channel_f = request.GET.get('channel', '')
    if channel_f:
        alerts = alerts.filter(channel=channel_f)

    return render(request, 'portal_app/notifications.html', {
        'alerts': alerts,
        'channel_f': channel_f,
    })


@login_required
def mark_notification_read_view(request, notif_id):
    alert = get_object_or_404(CaseEventNotification, id=notif_id)
    alert.is_read = True
    alert.save()
    return redirect('notifications')
