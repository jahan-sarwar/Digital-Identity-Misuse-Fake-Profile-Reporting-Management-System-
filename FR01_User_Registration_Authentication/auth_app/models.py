from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ==============================================================================
# Model: UserProfile (ব্যবহারকারীর প্রোফাইল এক্সটেনশন)
# Extends standard Django User with contact details and Admin Account Approval
# সাধারণ জ্যাঙ্গো ইউজারের সাথে ফোন, জাতীয় পরিচয়পত্র ও অ্যাডমিন অনুমোদন অবস্থা যুক্ত করে
# ==============================================================================
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    APPROVAL_CHOICES = (
        ('PENDING', 'Pending Approval / অপেক্ষমাণ'),
        ('APPROVED', 'Approved / অনুমোদিত'),
        ('REJECTED', 'Rejected / প্রত্যাখ্যাত'),
    )

    # OneToOne link to Django auth User / জ্যাঙ্গো ইউজার মডেলের সাথে ওয়ান-টু-ওয়ান সম্পর্ক
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Contact phone number / যোগাযোগের ফোন নম্বর
    phone_number = models.CharField(max_length=20, help_text="Contact Phone Number")
    
    # National ID or Passport number / জাতীয় পরিচয়পত্র বা পাসপোর্ট নম্বর
    nid_or_passport = models.CharField(max_length=50, blank=True, null=True, help_text="National ID or Passport")
    
    # Gender selection / লিঙ্গ নির্বাচন
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    # Date of birth / জন্ম তারিখ
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Physical address / বর্তমান বা স্থায়ী ঠিকানা
    address = models.TextField(blank=True, null=True)
    
    # User avatar image / প্রোফাইল ছবি
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Identity verified flag / পরিচয়পত্র যাচাইকৃত কি না
    is_identity_verified = models.BooleanField(default=False)
    
    # Admin approval status for account activation / অ্যাকাউন্ট সক্রিয়করণে অ্যাডমিন অনুমোদনের অবস্থা
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='PENDING')
    
    # Admin who approved this account / যে অ্যাডমিন অ্যাকাউন্টটি অনুমোদন করেছেন
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_user_profiles')
    
    # Approval timestamp / অনুমোদনের সময়
    approval_date = models.DateTimeField(null=True, blank=True)
    
    # Auto timestamps / স্বয়ংক্রিয় সময় সংরক্ষণ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username} ({self.get_approval_status_display()})"


# ==============================================================================
# Model: CaseReportRequest (পেন্ডিং কেস রিকোয়েস্ট মডেল)
# Stores complaint requests submitted by victims awaiting Admin acceptance
# ব্যবহারকারীর দেওয়া সাইবার বুলিং ও ফেক প্রোফাইল কেস যা অ্যাডমিন যাচাই করে এক্সেপ্ট করবেন
# ==============================================================================
class CaseReportRequest(models.Model):
    CASE_STATUS_CHOICES = (
        ('PENDING', 'Pending Acceptance / পর্যালোচনার অপেক্ষায়'),
        ('ACCEPTED', 'Accepted & Under Investigation / গৃহীত ও তদন্তাধীন'),
        ('REJECTED', 'Rejected & Dismissed / বাতিলকৃত'),
    )

    # Submitting user / যিনি কেস দাখিল করেছেন
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_cases')
    
    # Unique tracking case ID / কেস ট্র্যাকিং নম্বর
    case_number = models.CharField(max_length=40, unique=True)
    
    # Misuse platform / সোশ্যাল মিডিয়া প্ল্যাটফর্মের নাম (যেমন: Facebook, Instagram)
    platform = models.CharField(max_length=50)
    
    # Fake profile or content URL / ভুয়া প্রোফাইল বা কনটেন্টের লিংক
    fake_profile_url = models.URLField(max_length=500)
    
    # Incident detailed description / ঘটনার বিস্তারিত বিবরণ
    incident_description = models.TextField()
    
    # Additional evidence notes / প্রমাণের বিবরণ বা নোট
    evidence_notes = models.TextField(blank=True, null=True)
    
    # Status of the case request / কেসের বর্তমান অবস্থা
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES, default='PENDING')
    
    # Administrator review notes / অ্যাডমিনের মন্তব্য
    admin_notes = models.TextField(blank=True, null=True)
    
    # Admin who accepted/reviewed the case / কেস পর্যালোচনাকারী অ্যাডমিন
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_case_requests')
    
    # Review timestamp / কেস পর্যালোচনার সময়
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Creation and update timestamps / দাখিল ও হালনাগাদের সময়
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Case #{self.case_number} - {self.platform} ({self.get_status_display()})"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Auto-create profile when user is registered / নতুন ইউজার তৈরি হলে স্বয়ংক্রিয় প্রোফাইল তৈরি
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
