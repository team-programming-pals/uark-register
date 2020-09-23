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
	path('', views.signIn, name='signIn'), # Show the signIn page by default
	path('registerMenu/', views.registerMenu, name='registerMenu'),

	path('productListing/', views.productListing, name='productListing'),
	path('productDetails/<uuid:productUUID>/', views.productDetails, name='productDetails'),
	path('productCreate/', views.productCreate, name='productCreate'),

	path('employeeDetails/', views.employeeDetails, name='employeeDetails'),
	path('signIn/', views.signIn, name='signIn'),
	path('signOff/', views.signOff, name='signOff'),

	path('api/', include(router.urls)), # This will automatically route traffic for any number of API endpoints
	path('api/<uuid:id>/', include(router.urls)), # This is for API endpoint requests that pass along an id
	path('admin/', admin.site.urls), # This will route the traffic to the Django admin panel

]

# Display a custom template when a page is not found
handler404 = views.register_404