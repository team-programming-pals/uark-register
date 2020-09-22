"""
Helpful Resources:

    1. https://docs.djangoproject.com/en/3.1/topics/http/urls/
    2. https://www.django-rest-framework.org/tutorial/quickstart/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from register import views


# Create a router so our API endpoint(s) can automatically route traffic
router = routers.DefaultRouter()

# Register our products API with the rest framework
router.register(r'products', views.productViewSet)

# Tell Django how to route traffic to specific pages
urlpatterns = [
	path('', views.productListing, name='productListing'), # This is the default page that will be displayed
	path('api/<uuid:id>/', include(router.urls)), # This is for API endpoint requests that pass along an id
	path('api/', include(router.urls)), # This will automatically route traffic for any number of API endpoints
	path('admin/', admin.site.urls), # This will route the traffic to the Django admin panel
	path('productDetails/<uuid:productUUID>/', views.productDetails, name='productDetails'), # This is the product details page
	path('productCreate/', views.productCreate, name='productCreate'), # This is the product creation page
]
