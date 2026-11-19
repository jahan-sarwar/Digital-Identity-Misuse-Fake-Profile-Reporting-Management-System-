from django.contrib import admin
from .models import UserProfile, CaseReportRequest

# ==============================================================================
# Django Admin Configuration: UserProfile
# অ্যাডমিন প্যানেলে ব্যবহারকারী প্রোফাইল এবং অ্যাকাউন্ট অনুমোদন পরিচালনা
# ==============================================================================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'nid_or_passport', 'approval_status', 'is_identity_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number', 'nid_or_passport')
    list_filter = ('approval_status', 'is_identity_verified', 'gender')
    actions = ['approve_selected_accounts']

    # Admin bulk action to approve accounts / একসাথে একাধিক অ্যাকাউন্ট অনুমোদন করার অ্যাকশন
    @admin.action(description="Approve selected user accounts / নির্বাচিত অ্যাকাউন্ট অনুমোদন করুন")
    def approve_selected_accounts(self, request, queryset):
        for profile in queryset:
            profile.approval_status = 'APPROVED'
            profile.approved_by = request.user
            profile.save()
            profile.user.is_active = True
            profile.user.save()


# ==============================================================================
# Django Admin Configuration: CaseReportRequest
# অ্যাডমিন প্যানেলে দাখিলকৃত কেস রিকোয়েস্ট এবং পর্যালোচনা পরিচালনা
# ==============================================================================
@admin.register(CaseReportRequest)
class CaseReportRequestAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'reporter', 'platform', 'status', 'created_at')
    search_fields = ('case_number', 'reporter__username', 'platform', 'incident_description')
    list_filter = ('status', 'platform', 'created_at')
