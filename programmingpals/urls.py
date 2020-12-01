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


# Create a router so our API endpoints can automatically route traffic
router = routers.DefaultRouter()

# Register our API end-points with DRF
router.register(r'products', views.productViewSet)
router.register(r'employees', views.employeeViewSet)
router.register(r'activeusers', views.activeUserViewSet)


urlpatterns = [

	# This route point to our default page
	path('', views.signIn, name='signIn'),

	# These routes point to pages tthat have a queryString passed to them
	path('employeeDetails/queryString=<str:queryString>/', views.employeeDetails, name='employeeDetails'),
	path('productListing/queryString=<str:queryString>/', views.productListing, name='productListing'),
	path('productDetails/queryString=<str:queryString>/', views.productDetails, name='productDetails'),
	path('productCreate/queryString=<str:queryString>/', views.productCreate, name='productCreate'),
	path('registerMenu/queryString=<str:queryString>/', views.registerMenu, name='registerMenu'),
	path('transactionMenu/queryString=<str:queryString>/', views.transactionMenu, name='transactionMenu'),
	path('signIn/queryString=<str:queryString>/', views.signIn, name='signIn'),

	# These routes point to pages that have some sort of ID passed to them
	path('productDetails/<uuid:productUUID>/', views.productDetails, name='productDetails'),
	path('employeeDetails/<int:employeeID>/', views.employeeDetails, name='employeeDetails'),
	path('signIn/<int:employeeID>/', views.signIn, name='signIn'),

	# These routes point to normal pages
	path('registerMenu/', views.registerMenu, name='registerMenu'),
	path('productListing/', views.productListing, name='productListing'),
	path('productDetails/', views.productCreate, name='productDetails'),
	path('productCreate/', views.productCreate, name='productCreate'),
	path('employeeDetails/', views.employeeDetails, name='employeeDetails'),
	path('transactionMenu/', views.transactionMenu, name='transactionMenu'),
	path('transactionDetails/', views.transactionDetails, name='transactionDetails'),
	path('addCartItem/', views.addCartItem, name='addCartItem'),
	path('deleteCartItem/', views.deleteCartItem, name='deleteCartItem'),
	path('updateCartQuantity/', views.updateCartQuantity, name='updateCartQuantity'),
    path('cancelTransaction/', views.cancelTransaction, name='cancelTransaction'),
	path('signIn/', views.signIn, name='signIn'),
	path('signOff/', views.signOff, name='signOff'),

	# This route exposes our APIs to the public
	path('api/', include(router.urls)),
	path('api/<uuid:id>/', include(router.urls)),

	# This route points to the Django administration panel
	path('admin/', admin.site.urls),

	# These routes will point to the employee management APIView
	path('employees/manage/', views.manageEmployees.as_view()),
	path('employees/manage/<uuid:employeeUUID>/', views.manageEmployees.as_view()),

	# These routes point to the product management APIView
	path('products/manage/', views.manageProducts.as_view()),
	path('products/manage/<uuid:productUUID>/', views.manageProducts.as_view()),
]

# Display a custom template when a page is not found
handler404 = views.register_404