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
def productListing(request, errorMessage='default'):
	return render(request, 'productListing.html', {'products': Product.objects.all(), 'errorMessage': errorMessage})


# Process all client requests made to /productDetails/<uuid:productUUID>/
def productDetails(request, productUUID, errorMessage='default'):
	return render(request, 'productDetails.html', {'product': get_object_or_404(Product, pk=productUUID), 'errorMessage': errorMessage})


# Process all client requests made to /productCreate/
def productCreate(request, errorMessage='default'):
	return render(request, 'productCreate.html', {'errorMessage': errorMessage})


# Process all client requests to /employeeDetails/
def employeeDetails(request, errorMessage='default'):
	return render(request, 'employeeDetails.html', {'errorMessage': errorMessage})


# Process all client requests made to the signIn page
def signIn(request, errorMessage='default'):
	# Listen for incoming POST requests
	if request.method == 'POST':

		# Grab the username and password from apiRequest.js
		employeeData = json.loads(request.body)

		# EmployeeID must be an integer
		if (employeeData['employeeID'].isdigit() == False):
			# The request failed. Return status code 403 FORBIDDEN to apiRequests.js
			return HttpResponse(json.dumps('Register Error: An employeeID must be a positive integer'), status=403)

		# Do not accept a blank employeeID
		if (employeeData['employeeID'] == ''):
			# The request failed. Return status code 403 FORBIDDEN to apiRequests.js
			return HttpResponse(json.dumps('Register Error: You must enter an employeeID.'), status=403)

		# Do not accept a blank password
		if (employeeData['employeePassword'] == ''):
			# The request failed. Return status code 403 FORBIDDEN to apiRequests.js
			return HttpResponse(json.dumps('Register Error: You must enter a password.'), status=403)

		# Check if an employee account with the provided employeeID and password exists
		employee = Employee.objects.filter(employeeID=employeeData['employeeID'], 
											employeePassword=employeeData['employeePassword'])

		if (employee.exists()):
			# Create a new session for the active employee if one does not already exist
			if (not request.session.session_key):
				request.session.create()

			# Do not let orphaned sessions break the register
			if (request.session.session_key == None):
				request.session.create()

			# Set the employeeID as a session variable. This is required for the signOff function
			request.session['employeeID'] = employeeData['employeeID']

			# Get information about the user who just signed into the system
			activeEmployee = Employee.objects.get(employeeID=employeeData['employeeID'])

			# Combine the FirstName and LastName into one variable to make the active name
			activeName = ('{} {}').format(str(activeEmployee.employeeFirstName), str(activeEmployee.employeeLastName))

			# Check if the employee already has an ActiveUser database record
			activeSessionCheck = ActiveUser.objects.filter(activeEmployeeUUID=activeEmployee.employeeUUID)


			if (activeSessionCheck.exists()):
				# Update the employees ActiveUser session key
				ActiveUser.objects.filter(activeEmployeeUUID=activeEmployee.employeeUUID).update(activeSessionKey=request.session.session_key)
			else:
				# Create a new ActiveUser database record for the employee
				activeUser = ActiveUser.objects.create(activeEmployeeUUID=activeEmployee.employeeUUID,
														activeName=activeName,
														activeClassification=activeEmployee.employeeClassification,
														activeSessionKey=request.session.session_key)

			# Mark the employee as active
			Employee.objects.filter(employeeID=activeEmployee.employeeID).update(employeeActive=True)

			# The request was successful. Return status code 200 OK back to apiRequests.js
			return HttpResponse({}, status=200)
		else:
			# The request failed. Return status code 403 FORBIDDEN to apiRequests.js
			return HttpResponse({json.dumps('Register Error: Incorrect username or password')}, status=403)

	# Transforms signin.html into an httpResponse object gunicorn can render as a web page
	return render(request, 'signin.html', {'employees': Employee.objects.all(), 'errorMessage': errorMessage})


# Process all client requests made to the signOff page
def signOff(request):
	# Only try to clean up if there is an active session
	if (request.session.session_key):
		# Delete the employee from the ActiveUsers database
		ActiveUser.objects.filter(activeSessionKey=request.session.session_key).delete()

		# Mark the employee as inactive
		Employee.objects.filter(employeeID=request.session['employeeID']).update(employeeActive=False)

		# Call Djangos built-in logout function to delete session information
		logout(request)

	# Redirect the user to the main page
	return HttpResponseRedirect('/signIn')


# Process all client requests for the main menu
def registerMenu(request, errorMessage='default'):
	if (not request.session.session_key):
		# Redirect to the sign in page if the user is not signed into the register
		return signIn(request, 'You must be signed into the register to access the main menu.')

	# There is an active session, so render the main menu
	return render(request, 'registerMenu.html')

	
# Process all client requests for page not found errors
def register_404(request, exception):
	return render(request, 'register_404.html')