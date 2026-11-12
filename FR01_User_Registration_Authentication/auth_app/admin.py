from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'nid_or_passport', 'is_identity_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    list_filter = ('is_identity_verified', 'gender')

