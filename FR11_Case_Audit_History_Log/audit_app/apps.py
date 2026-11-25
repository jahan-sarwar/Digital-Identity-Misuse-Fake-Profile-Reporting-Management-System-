# Audit application metadata
from django.apps import AppConfig

class AuditAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audit_app'
    verbose_name = 'Case Audit History and Activity Log'
