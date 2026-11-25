# Initial database migration for SecurityAuditTrail
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SecurityAuditTrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.CharField(db_index=True, help_text='Associated Incident Case ID', max_length=32)),
                ('action_category', models.CharField(choices=[('CASE_SUBMITTED', 'Initial Incident Report Logged'), ('EVIDENCE_UPLOADED', 'Forensic Evidence Asset Uploaded'), ('IDENTITY_VERIFIED', 'Complainant Identity Authenticated'), ('ASSIGNED_TO_OFFICER', 'Investigator Staff Allocated'), ('STATUS_TRANSITION', 'Investigation Milestone Advanced'), ('EVIDENCE_INSPECTED', 'Evidence Hash Cryptographically Inspected'), ('PLATFORM_TAKEDOWN_ISSUED', 'Formal Platform Subpoena Transmitted'), ('RESOLUTION_CLOSED', 'Case Successfully Closed & Neutralized')], default='STATUS_TRANSITION', max_length=35)),
                ('actor_username', models.CharField(help_text='Username of officer or citizen', max_length=100)),
                ('actor_role', models.CharField(default='Lead Forensic Detective', help_text='Role designation', max_length=80)),
                ('ip_address', models.GenericIPAddressField(default='127.0.0.1', help_text='Client IP address')),
                ('user_agent', models.CharField(blank=True, help_text='Browser/Client User-Agent fingerprint', max_length=255)),
                ('previous_state', models.CharField(blank=True, help_text='State before action execution', max_length=100)),
                ('new_state', models.CharField(blank=True, help_text='State resulting from action execution', max_length=100)),
                ('action_narrative', models.TextField(help_text='Detailed audit statement describing the transaction')),
                ('event_hash', models.CharField(blank=True, help_text='SHA-256 hash ensuring tamper-proof record', max_length=64)),
                ('is_tamper_verified', models.BooleanField(default=True, help_text='Verified against blockchain/system digest')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
