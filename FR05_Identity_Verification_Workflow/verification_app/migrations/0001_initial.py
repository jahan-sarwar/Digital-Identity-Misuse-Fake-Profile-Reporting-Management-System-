# Database migration for IdentityVerification model
import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='IdentityVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('case_id', models.CharField(help_text='Case ID associated with the identity report', max_length=32)),
                ('reporter_full_name', models.CharField(help_text='Legal full name of the complainant', max_length=150)),
                ('reporter_email', models.EmailField(help_text='Active email address for verification updates', max_length=254)),
                ('reporter_phone', models.CharField(blank=True, help_text='Contact number for SMS/OTP verification', max_length=20)),
                ('document_type', models.CharField(choices=[('NID', 'National Identification Card (NID)'), ('PASSPORT', 'International Passport'), ('DRIVING_LICENSE', 'Driving License'), ('STUDENT_ID', 'Institutional / Student ID Card'), ('OFFICIAL_BADGE', 'Government or Corporate Security Badge')], default='NID', max_length=30)),
                ('id_number', models.CharField(help_text='Document serial or registration number', max_length=50)),
                ('document_file', models.FileField(help_text='Scanned copy of official ID card/passport', upload_to='identity_docs/%Y/%m/')),
                ('selfie_photo', models.ImageField(help_text='Clear selfie photograph holding the case ID', upload_to='identity_selfies/%Y/%m/')),
                ('verification_status', models.CharField(choices=[('PENDING', 'Pending Administrative Review'), ('UNDER_REVIEW', 'Under Document Forensic Verification'), ('VERIFIED', 'Officially Verified & Authenticated'), ('REJECTED', 'Verification Rejected / Discrepancy Found')], default='PENDING', max_length=25)),
                ('admin_notes', models.TextField(blank=True, help_text='Internal remarks by verification officer')),
                ('rejection_reason', models.CharField(blank=True, help_text='Reason if document verification fails', max_length=255)),
                ('reviewed_by', models.CharField(blank=True, help_text='Name of investigating officer', max_length=100)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-submitted_at'],
            },
        ),
    ]
