# Dashboard app config
from django.apps import AppConfig

class DashboardAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard_app'
    verbose_name = 'Administrative Dashboard and User Approval'
