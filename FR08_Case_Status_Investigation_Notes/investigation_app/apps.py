# Application configuration
from django.apps import AppConfig

class InvestigationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investigation_app'
    verbose_name = 'Investigation Status and Case Notes'
