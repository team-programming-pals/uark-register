"""
Helpful Resources:

    1. https://docs.djangoproject.com/en/3.1/ref/applications/
"""
from django.apps import AppConfig


# Make our register a pluggable web application
class RegisterConfig(AppConfig):
    name = 'register'
    verbose_name = 'Uark Register'
