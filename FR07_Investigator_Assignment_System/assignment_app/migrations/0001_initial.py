# Database migration for Investigator Assignment System
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='InvestigatorStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Full legal name of the investigator', max_length=120)),
                ('badge_number', models.CharField(help_text='Official investigative badge number', max_length=40, unique=True)),
                ('email', models.EmailField(help_text='Official department email', max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, help_text='Direct desk/mobile contact', max_length=20)),
                ('rank_title', models.CharField(default='Cyber Forensic Investigator', help_text='Official rank/designation', max_length=80)),
                ('specialization', models.CharField(choices=[('SOCIAL_MEDIA_FRAUD', 'Social Media Fraud & Clone Profiles'), ('CYBER_EXTORTION', 'Blackmail & Financial Cyber Extortion'), ('DEFAMATION_HARASSMENT', 'Online Harassment & Slander'), ('CORPORATE_IDENTITY_THEFT', 'Executive Impersonation & Brand Theft')], default='SOCIAL_MEDIA_FRAUD', max_length=50)),
                ('active_caseload', models.PositiveIntegerField(default=0, help_text='Number of active cases currently handled')),
                ('max_caseload_capacity', models.PositiveIntegerField(default=5, help_text='Maximum simultaneous active cases')),
                ('is_available', models.BooleanField(default=True, help_text='Available for immediate case allocation')),
            ],
        ),
        migrations.CreateModel(
            name='CaseAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.CharField(help_text='Incident Case ID to be assigned', max_length=32, unique=True)),
                ('title', models.CharField(help_text='Headline / Brief summary of identity misuse', max_length=200)),
                ('platform', models.CharField(default='Facebook', help_text='Target platform of misuse', max_length=50)),
                ('priority', models.CharField(choices=[('LOW', 'Low Priority (Standard SLA: 7 Days)'), ('MEDIUM', 'Medium Priority (SLA: 72 Hours)'), ('HIGH', 'High Priority (SLA: 24 Hours)'), ('URGENT', 'Urgent / Emergency Escalation (SLA: 6 Hours)')], default='MEDIUM', max_length=20)),
                ('assignment_status', models.CharField(choices=[('UNASSIGNED', 'Unassigned / In Triage Pool'), ('ASSIGNED', 'Assigned to Investigator'), ('ACCEPTED_BY_OFFICER', 'Accepted by Assigned Officer'), ('IN_PROGRESS', 'Active Investigation Underway'), ('COMPLETED', 'Investigation Completed & Closed')], default='UNASSIGNED', max_length=30)),
                ('assigned_by', models.CharField(default='Admin Controller', help_text='Name/ID of assigning supervisor', max_length=100)),
                ('supervisor_directives', models.TextField(blank=True, help_text='Specific forensic instructions for the investigator')),
                ('assigned_at', models.DateTimeField(blank=True, null=True)),
                ('deadline_date', models.DateField(blank=True, help_text='Target date for case resolution', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_investigator', models.ForeignKey(blank=True, help_text='Investigating officer assigned to this case', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_cases', to='assignment_app.investigatorstaff')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
