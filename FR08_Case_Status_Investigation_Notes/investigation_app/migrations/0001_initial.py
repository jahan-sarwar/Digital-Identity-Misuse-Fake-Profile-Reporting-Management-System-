# Initial database migration for Investigation models
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='InvestigationCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.CharField(help_text='Unique Case Reference Number', max_length=32, unique=True)),
                ('case_title', models.CharField(help_text='Subject title of the complaint', max_length=200)),
                ('victim_name', models.CharField(help_text='Complainant legal name', max_length=150)),
                ('investigating_officer', models.CharField(default='Inspector Sarwar', help_text='Assigned Officer Name', max_length=100)),
                ('current_status', models.CharField(choices=[('ASSIGNED', 'Assigned - Initial Briefing'), ('IN_PROGRESS', 'Forensic Analysis In Progress'), ('EVIDENCE_VERIFIED', 'Digital Evidence Confirmed'), ('LEGAL_NOTICE_SENT', 'Platform Legal Takedown Notice Issued'), ('ESCALATED_TO_PLATFORM', 'Escalated to Global Trust & Safety Desk'), ('RESOLVED', 'Offending Profile Neutralized / Resolved'), ('CLOSED_UNRESOLVED', 'Case Closed / Inconclusive Evidence')], default='IN_PROGRESS', max_length=35)),
                ('suspect_lead_info', models.TextField(blank=True, help_text='Forensic details: ISP, IP logs, suspected handle aliases')),
                ('platform_takedown_requested', models.BooleanField(default=False, help_text='Formal takedown ticket submitted')),
                ('platform_ticket_id', models.CharField(blank=True, help_text='Platform legal case ticket ID', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='InvestigationNoteEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('officer_name', models.CharField(help_text='Name of logging investigator', max_length=100)),
                ('note_type', models.CharField(choices=[('STATUS_CHANGE', 'Status Transition & Operational Event'), ('FORENSIC_EXAMINATION', 'Digital Forensic / OSINT Finding'), ('PLATFORM_CORRESPONDENCE', 'Platform Communication / Subpoena Response'), ('INTERVIEW_DEPOSITION', 'Complainant or Witness Interview Note'), ('INTERNAL_STRATEGY', 'Confidential Legal Strategy Memo')], default='FORENSIC_EXAMINATION', max_length=30)),
                ('is_confidential', models.BooleanField(default=False, help_text='Restricted to senior forensic officers')),
                ('previous_status', models.CharField(blank=True, max_length=40)),
                ('new_status', models.CharField(blank=True, max_length=40)),
                ('detailed_notes', models.TextField(help_text='Comprehensive investigative findings and observations')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(help_text='Investigation case record', on_delete=django.db.models.deletion.CASCADE, related_name='investigation_notes', to='investigation_app.investigationcase')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
