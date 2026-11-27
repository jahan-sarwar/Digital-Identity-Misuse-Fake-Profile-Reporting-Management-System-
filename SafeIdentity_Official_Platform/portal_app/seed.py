# Idempotent master admin initialization - Zero dummy/demo cases or fake data
from django.contrib.auth.models import User


def ensure_seed_data():
    """
    Ensures a clean, production-ready initial state.
    Creates ONLY the Master Administrator account if no admin exists.
    Zero dummy cases, zero fake notifications, zero fake audit trails are created.
    """
    # 1. Master Administrator (sarwar)
    if not User.objects.filter(username='admin.sarwar').exists():
        admin_sarwar = User.objects.create_superuser(
            username='admin.sarwar',
            email='admin.sarwar@safeidentity.org',
            password='Admin@1234',
            first_name='Sarwar Jahan'
        )
        admin_sarwar.is_staff = True
        admin_sarwar.is_superuser = True
        admin_sarwar.save()
        profile = admin_sarwar.profile
        profile.role = 'ADMIN'
        profile.is_approved = True
        profile.approval_status = 'APPROVED'
        profile.badge_number = 'ADM-001'
        profile.phone_number = '+880 1718-000014'
        profile.is_identity_verified = True
        profile.save()

    # 2. Master Administrator alias (admin)
    if not User.objects.filter(username='admin').exists():
        admin_default = User.objects.create_superuser(
            username='admin',
            email='admin@safeidentity.org',
            password='Admin@1234',
            first_name='System Administrator'
        )
        admin_default.is_staff = True
        admin_default.is_superuser = True
        admin_default.save()
        profile_def = admin_default.profile
        profile_def.role = 'ADMIN'
        profile_def.is_approved = True
        profile_def.approval_status = 'APPROVED'
        profile_def.badge_number = 'ADM-000'
        profile_def.is_identity_verified = True
        profile_def.save()
