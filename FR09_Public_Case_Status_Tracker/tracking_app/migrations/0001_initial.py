# Initial database migration for TrackableCase
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='TrackableCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.CharField(help_text='Public Case Reference ID', max_length=32, unique=True)),
                ('security_pin', models.CharField(default='123456', help_text='6-digit verification PIN provided to citizen', max_length=6)),
                ('complainant_name', models.CharField(max_length=150)),
                ('complainant_email', models.EmailField(max_length=254)),
                ('platform_name', models.CharField(default='Facebook', max_length=50)),
                ('impersonated_account_name', models.CharField(max_length=150)),
                ('progress_stage', models.CharField(choices=[('1_SUBMITTED', '1. Complaint Registered'), ('2_VERIFIED', '2. Complainant Identity Authenticated'), ('3_ASSIGNED', '3. Allocated to Forensic Investigator'), ('4_INVESTIGATION', '4. Forensic Examination & Platform Takedown Active'), ('5_RESOLVED', '5. Offending Profile Neutralized & Case Resolved')], default='1_SUBMITTED', max_length=30)),
                ('public_status_message', models.CharField(default='Your complaint has been logged and is awaiting document triage.', help_text='Public-facing explanation displayed to citizen', max_length=255)),
                ('assigned_agency', models.CharField(default='National Cyber Crime Investigation Division', max_length=100)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('last_status_update', models.DateTimeField(auto_now=True)),
                ('estimated_completion_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-submission_date'],
            },
        ),
    ]
