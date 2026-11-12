import uuid
from django.db import models

class PlatformReport(models.Model):
    """
    Model storing platform selection, reported URL, username handle, and case tracking code.
    """
    PLATFORM_CHOICES = (
        ('FACEBOOK', 'Facebook'),
        ('INSTAGRAM', 'Instagram'),
        ('TWITTER', 'Twitter / X'),
        ('TIKTOK', 'TikTok'),
        ('LINKEDIN', 'LinkedIn'),
        ('YOUTUBE', 'YouTube'),
        ('TELEGRAM', 'Telegram'),
        ('WHATSAPP', 'WhatsApp'),
        ('OTHER', 'Other Social Platform'),
    )

    case_id = models.CharField(max_length=32, unique=True, editable=False)
    reporter_name = models.CharField(max_length=150, help_text="Reporter Name")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, help_text="Social media platform")
    other_platform_name = models.CharField(max_length=100, blank=True, null=True, help_text="If Other, specify platform name")
    target_profile_url = models.URLField(max_length=500, help_text="Direct link to fake profile or post")
    target_username_or_handle = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., @fake_victim")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.case_id:
            self.case_id = f"DIM-2026-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.case_id}] {self.get_platform_display()} - {self.target_username_or_handle or self.target_profile_url}"

