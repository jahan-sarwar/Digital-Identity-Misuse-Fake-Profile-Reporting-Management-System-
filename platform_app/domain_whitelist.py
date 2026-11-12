"""
Platform Domain Whitelist Configuration.
Maintains authorized domain lists for all major supported platforms.
"""

PLATFORM_DOMAINS = {
    'FACEBOOK': ['facebook.com', 'fb.com', 'fb.watch', 'm.facebook.com'],
    'INSTAGRAM': ['instagram.com', 'instagr.am'],
    'TWITTER': ['twitter.com', 'x.com'],
    'TIKTOK': ['tiktok.com', 'vm.tiktok.com'],
    'LINKEDIN': ['linkedin.com'],
    'YOUTUBE': ['youtube.com', 'youtu.be'],
    'TELEGRAM': ['t.me', 'telegram.me'],
    'WHATSAPP': ['whatsapp.com', 'wa.me'],
}

def get_allowed_domains_for_platform(platform_key):
    """Returns list of allowed domains for a given platform key."""
    return PLATFORM_DOMAINS.get(platform_key, [])

