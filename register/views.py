"""
Helpful Resources:

	1. https://docs.djangoproject.com/en/3.1/topics/db/models/
	2. https://docs.djangoproject.com/en/3.1/topics/class-based-views/
	3. https://www.django-rest-framework.org/tutorial/quickstart/
	4. https://docs.djangoproject.com/en/3.1/topics/http/shortcuts/
"""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from .serializers import productSerializer, employeeSerializer, ActiveUserSerializer
from .models import Product, Employee, ActiveUser
import hashlib
import json

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

	# Convert database information into native python data types that can be easily converted to JSON
	serializer_class = productSerializer


# Process all client requests made to our employee API
class employeeViewSet(viewsets.ModelViewSet):
	"""
	An API endpoint which will allow us to view or edit
	employees in our database. The incoming HTTP verb
	determines the behavior of this function:

	1. GET: Will ask the view to return information from the database
	2. POST: Will ask the view to create a new employee and add it to the database
	3. PUT: Will ask the view to modify an existing employee in the database
	4. PATCH: Will ask the view to modify an individual field of a employee that exists in the database
	5. DELETE: Will ask the view to delete a specific employee from the database 
	"""

	# Map primitive user input into a model instance or all writable relational fields
	queryset = Employee.objects.all()

	# Convert database information into native python data types that can be easily converted to JSON
	serializer_class = employeeSerializer


# Process all client requests made to our active users API
class activeUserViewSet(viewsets.ModelViewSet):
	"""
	An API endpoint which will allow us to view or edit
	active users in our database. The incoming HTTP verb
	determines the behavior of this function:

	1. GET: Will ask the view to return information from the database
	2. POST: Will ask the view to create a new active user and add it to the database
	3. PUT: Will ask the view to modify an existing active user in the database
	4. PATCH: Will ask the view to modify an individual field of an active user that exists in the database
	5. DELETE: Will ask the view to delete a specific active user from the database 
	"""

	# Map primitive user input into a model instance or all writable relational fields
	queryset = ActiveUser.objects.all()

	# Convert database information into native python data types that can be easily converted to JSON
	serializer_class = ActiveUserSerializer


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


def employeeDetails(request):
	# Transforms employeeDetails.html into an httpResponse object gunicorn can render as a web page
	return render(request, 'employeeDetails.html')


# Process all client requests made to the signIn page
def signIn(request):
	# Listen for incoming POST requests
	if request.method == 'POST':

		# Grab the username and password from apiRequest.js
		employeeData = json.loads(request.body)

		# Query the database and store the result in the employee object
		employee = Employee.objects.filter(employeeID=employeeData['employeeID'], 
											employeePassword=employeeData['employeePassword'])

		# Route the request in a way apiRequest.js can understand it
		if (employee.exists()):
			# Get information about the user who just signed into the system
			activeEmployee = Employee.objects.get(employeeID=employeeData['employeeID'])

			# Combine the FirstName and LastName into one variable
			activeName = ('{} {}').format(str(activeEmployee.employeeFirstName), str(activeEmployee.employeeLastName))

			# Delete any orphaned active sessions the user may have left behind
			activeSessionCheck = ActiveUser.objects.filter(activeEmployeeUUID=activeEmployee.employeeUUID).delete()

			# Create a new session for the active user.
			if (not request.session.session_key):
				request.session['employeeID'] = activeEmployee.employeeID
				request.session.create()

			# Update the employees active status
			activeEmployee.employeeActive = True
			activeEmployee.save()

			# Place the user in the ActiveUsers database
			activeUser = ActiveUser.objects.create(activeEmployeeUUID=activeEmployee.employeeUUID,
													activeName=activeName,
													activeClassification=activeEmployee.employeeClassification,
													activeSessionKey=request.session.session_key)

			return HttpResponse({}, status=200)
		else:
			return HttpResponse({}, status=403)

	# Transforms signin.html into an httpResponse object gunicorn can render as a web page
	return render(request, 'signin.html', {'employees': Employee.objects.all()})


def signOff(request):
	# Only try to clean up if there is an active session
	if ('employeeID' in request.session):
		# Delete the active user session
		activeUser = ActiveUser.objects.filter(activeSessionKey=request.session.session_key).delete()

		# Check for the active users employee records
		checkStatus = Employee.objects.filter(employeeID=request.session['employeeID'])

		# Update the employees active status if there is a record of it
		if (checkStatus.exists()):
			updateEmployeeStatus = Employee.objects.get(employeeID=request.session['employeeID'])
			updateEmployeeStatus.employeeActive = False
			updateEmployeeStatus.save()

		# Call Djangos built-in logout function to delete session information
		logout(request)

	# Redirect the user to the main page
	return HttpResponseRedirect('/signIn')


def registerMenu(request):
	return render(request, 'registerMenu.html')

	
# Process all client requests for page not found errors
def register_404(request, exception):
	return render(request, 'register_404.html')