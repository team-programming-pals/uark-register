"""
Helpful Resources:

    1. https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application
from os import environ


# Register our web application with any WSGI-compliant web server
environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmingpals.settings')
application = get_wsgi_application()
