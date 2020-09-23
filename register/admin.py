"""
Helpful Resources:

    1. https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
"""
from django.contrib import admin
from .models import Product, Employee, ActiveUser


"""
Plug our models into the Django admin
module so we can access the database directly
from the administration panel
"""
admin.site.register(Product)
admin.site.register(Employee)
admin.site.register(ActiveUser)