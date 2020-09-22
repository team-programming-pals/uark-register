"""
Helpful Resources:

	1. https://docs.djangoproject.com/en/3.1/topics/db/models/
	2. https://docs.djangoproject.com/en/3.1/topics/class-based-views/
	3. https://www.django-rest-framework.org/tutorial/quickstart/
	4. https://docs.djangoproject.com/en/3.1/topics/http/shortcuts/
"""
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .serializers import productSerializer
from .models import Product


# Process all client requests made to our product API
class productViewSet(viewsets.ModelViewSet):
	"""
	An API endpoint which will allow us to view or edit
	products in our database. The incoming HTTP verb
	determines the behavior of this function:

	1. GET: Will ask the view to return information from the database
	2. POST: Will ask the view to create a new Product and add it to the database
	3. PUT: Will ask the view to modify an existing product in the database
	4. PATCH: Will ask the view to modify an individual field of a product that exists in the database
	5. DELETE: Will ask the view to delete a specific product from the database 
	"""

	# Map primitive user input into a model instance or all writable relational fields
	queryset = Product.objects.all()

	# Tell the endpoint how we would like to serialize information
	serializer_class = productSerializer


# Process all client requests made to the default register page
def productListing(request):
	"""
	Combines productListing.html with a dictionary that has all
	of the products from the database and returns an httpResponse
	object that gunicorn can render as a web page
	"""
	return render(request, 'productListing.html', {'products': Product.objects.all()})

# Process all client requests made to /productDetails/<uuid:productUUID>/
def productDetails(request, productUUID):
	"""
	Combines productDetail.html with a dictionary that has a
	single product from our database and returns an httpResponse
	object that gunicorn can render as a web page
	"""
	return render(request, 'productDetails.html', {'product': get_object_or_404(Product, pk=productUUID)})


# Process all client requests made to /productCreate/
def productCreate(request):
	# Transforms productCreate.html into an httpResponse object gunicorn can render as a web page
	return render(request, 'productCreate.html')
