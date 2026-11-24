# Initial database migration for User Account Approval and Dashboard models
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='AdministrativeCaseMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_title', models.CharField(max_length=100)),
                ('metric_value', models.PositiveIntegerField(default=0)),
                ('category', models.CharField(default='SYSTEM', max_length=50)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SystemUserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='Unique system login username', max_length=100, unique=True)),
                ('full_name', models.CharField(help_text='Legal full name of user', max_length=150)),
                ('email', models.EmailField(help_text='Official email address', max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, help_text='Contact telephone/mobile', max_length=20)),
                ('password_hash', models.CharField(help_text='Cryptographically hashed password', max_length=128)),
                ('assigned_role', models.CharField(choices=[('CITIZEN_REPORTER', 'Citizen / Complainant Reporter'), ('FORENSIC_INVESTIGATOR', 'CID Cyber Forensic Investigator'), ('TRIAGE_SUPERVISOR', 'Triage & Case Review Supervisor'), ('SYSTEM_ADMINISTRATOR', 'Security System Administrator')], default='CITIZEN_REPORTER', max_length=35)),
                ('department', models.CharField(blank=True, default='General Public / External', max_length=100)),
                ('is_approved', models.BooleanField(default=False, help_text='Access blocked unless approved by Admin')),
                ('approval_status', models.CharField(choices=[('PENDING_APPROVAL', 'Pending Security Administrator Approval'), ('APPROVED', 'Account Officially Approved & Active'), ('SUSPENDED', 'Account Temporarily Suspended'), ('REJECTED', 'Registration Application Rejected')], default='PENDING_APPROVAL', max_length=25)),
                ('admin_approval_notes', models.TextField(blank=True, help_text='Remarks by approving security administrator')),
                ('approved_by', models.CharField(blank=True, help_text='Name of reviewing admin', max_length=100)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-registered_at'],
            },
        ),
    ]
