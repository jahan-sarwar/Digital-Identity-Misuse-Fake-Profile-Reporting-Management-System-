# WSGI configuration for web server deployment
import os
from django.core.wsgi import get_wsgi_application

# Point to settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()
