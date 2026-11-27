# Module 03: Social Media Platform Selection & Target Profile URL Helpers
from portal_app.models import IncidentCase


def get_supported_platforms():
    # Return all configured social platforms from the unified model
    return IncidentCase.PLATFORM_CHOICES
