# Initial database migration for CaseEventNotification
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CaseEventNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.CharField(help_text='Associated Incident Case ID', max_length=32)),
                ('recipient_name', models.CharField(help_text='Complainant or Officer Name', max_length=150)),
                ('recipient_email', models.EmailField(help_text='Destination email address', max_length=254)),
                ('recipient_phone', models.CharField(blank=True, help_text='SMS phone number', max_length=20)),
                ('event_type', models.CharField(choices=[('CASE_SUBMITTED', 'Incident Report Registration Confirmed'), ('EVIDENCE_VERIFIED', 'Identity & Supporting Evidence Verified'), ('INVESTIGATOR_ASSIGNED', 'Investigating Officer Allocated'), ('TAKEDOWN_REQUESTED', 'Platform Legal Takedown Notice Issued'), ('STATUS_UPDATED', 'Milestone Progression Updated'), ('CASE_RESOLVED', 'Fraudulent Profile Neutralized / Closed')], default='STATUS_UPDATED', max_length=35)),
                ('notification_channel', models.CharField(choices=[('EMAIL', 'Official Email Dispatch'), ('SMS', 'Emergency SMS Gateway Alert'), ('IN_APP', 'Citizen Secure Dashboard Inbox'), ('SYSTEM_WEBHOOK', 'Automated Law Enforcement Webhook')], default='EMAIL', max_length=25)),
                ('subject', models.CharField(help_text='Notification alert headline', max_length=200)),
                ('message_body', models.TextField(help_text='Full notification text received by user')),
                ('delivery_status', models.CharField(choices=[('QUEUED', 'Queued in Dispatch Buffer'), ('SENT', 'Successfully Dispatched'), ('DELIVERED', 'Delivered & Acknowledged by Carrier'), ('FAILED', 'Transmission Failed / Bounced')], default='DELIVERED', max_length=20)),
                ('is_read', models.BooleanField(default=False, help_text='Marked as read in citizen inbox')),
                ('dispatched_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-dispatched_at'],
            },
        ),
    ]
