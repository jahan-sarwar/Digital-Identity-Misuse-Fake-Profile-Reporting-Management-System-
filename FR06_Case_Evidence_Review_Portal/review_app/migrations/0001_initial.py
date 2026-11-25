# Initial migration for IncidentReviewCase model
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='IncidentReviewCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.CharField(help_text='Unique Case Reference Number', max_length=32, unique=True)),
                ('complainant_name', models.CharField(help_text='Name of reporting citizen', max_length=150)),
                ('complainant_email', models.EmailField(help_text='Notification email address', max_length=254)),
                ('target_platform', models.CharField(choices=[('FACEBOOK', 'Facebook'), ('INSTAGRAM', 'Instagram'), ('LINKEDIN', 'LinkedIn'), ('TWITTER_X', 'X (Twitter)'), ('TIKTOK', 'TikTok'), ('WHATSAPP', 'WhatsApp / Telegram'), ('OTHER', 'Other Platform')], default='FACEBOOK', max_length=30)),
                ('fake_profile_url', models.URLField(help_text='Direct URL to reported fake profile', max_length=300)),
                ('impersonated_name', models.CharField(help_text='Name displayed on the fraudulent account', max_length=150)),
                ('incident_narrative', models.TextField(help_text='Full statement detailing the misuse incident')),
                ('risk_level', models.CharField(choices=[('LOW', 'Low Risk - Minor Misuse'), ('MEDIUM', 'Medium Risk - Impersonation Detected'), ('HIGH', 'High Risk - Financial / Reputational Extortion'), ('CRITICAL', 'Critical Risk - Severe Defamation / Identity Fraud')], default='MEDIUM', max_length=20)),
                ('review_status', models.CharField(choices=[('PENDING_TRIAGE', 'Pending Administrative Triage'), ('EVIDENCE_ACCEPTED', 'Evidence Validated & Accepted'), ('EVIDENCE_INSUFFICIENT', 'Insufficient Supporting Evidence'), ('UNDER_INVESTIGATION', 'Transferred to Forensics / Investigation'), ('DISMISSED', 'Dismissed / Ineligible Claim')], default='PENDING_TRIAGE', max_length=30)),
                ('evidence_count', models.PositiveIntegerField(default=1, help_text='Number of supporting files uploaded')),
                ('evidence_summary', models.CharField(blank=True, help_text='Summary of uploaded evidence types', max_length=255)),
                ('reviewer_notes', models.TextField(blank=True, help_text='Internal notes by review officer')),
                ('reviewed_by', models.CharField(blank=True, help_text='Username of triage administrator', max_length=100)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-submitted_at'],
            },
        ),
    ]
