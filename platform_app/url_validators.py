import re
from django.core.exceptions import ValidationError
from .domain_whitelist import PLATFORM_DOMAINS

def validate_platform_profile_url(platform, url):
    """
    Strict Validator ensuring submitted URL schema starts with http:// or https://
    and that the domain matches the selected platform.
    """
    if not url:
        raise ValidationError("Reported Profile URL is required.")

    clean_url = url.strip().lower()

    if not (clean_url.startswith('http://') or clean_url.startswith('https://')):
        raise ValidationError("Invalid URL protocol. Profile URL must start with 'http://' or 'https://'.")

    if platform in PLATFORM_DOMAINS:
        allowed = PLATFORM_DOMAINS[platform]
        if not any(domain in clean_url for domain in allowed):
            domains_str = ", ".join(allowed)
            raise ValidationError(
                f"The URL domain does not match the selected platform ({platform}). Must contain one of: {domains_str}"
            )

