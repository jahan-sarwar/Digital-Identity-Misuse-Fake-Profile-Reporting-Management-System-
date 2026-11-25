# Application metadata configuration
from django.apps import AppConfig

class AssignmentAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assignment_app'
    verbose_name = 'Investigator Assignment Module'
