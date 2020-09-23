"""
Helpful Resources:

    1. https://docs.djangoproject.com/en/3.1/topics/http/urls/
    2. https://www.django-rest-framework.org/tutorial/quickstart/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from rest_framework import routers
from register import views


# Create a router so our API endpoint(s) can automatically route traffic
router = routers.DefaultRouter()

# Register our products API with the rest framework
router.register(r'products', views.productViewSet)

# Register our employee API with the rest framework
router.register(r'employees', views.employeeViewSet)

# Register our active users API with the rest framework
router.register(r'activeusers', views.activeUserViewSet)


# Tell Django how to route traffic to specific pages
urlpatterns = [
	path('', views.productListing, name='productListing'), # This is the default page that will be displayed
	path('api/<uuid:id>/', include(router.urls)), # This is for API endpoint requests that pass along an id
	path('api/', include(router.urls)), # This will automatically route traffic for any number of API endpoints
	path('admin/', admin.site.urls), # This will route the traffic to the Django admin panel
	path('productDetails/<uuid:productUUID>/', views.productDetails, name='productDetails'), # This is the product details page
	path('productCreate/', views.productCreate, name='productCreate'), # This is the product creation page
	path('signIn/', views.signIn, name='signIn'), # This is the signIn page
	path('signOff/', views.signOff, name='signOff'), # This is the signOff page
]

# Display a custom template when a page is not found
handler404 = views.register_404