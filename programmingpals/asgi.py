"""
Helpful Resources:

	1. https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
from os import environ
from django.core.asgi import get_asgi_application


# Register our web application with any compliant, asynchronous web server
environ.setdefault('DJANGO_SETTINGS_MODULE', 'programmingpals.settings')
application = get_asgi_application()