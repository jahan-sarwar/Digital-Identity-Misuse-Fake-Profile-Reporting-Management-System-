# Tracking app config
from django.apps import AppConfig

class TrackingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracking_app'
    verbose_name = 'Public Case Status Tracker'
