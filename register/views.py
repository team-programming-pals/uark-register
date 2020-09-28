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
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import viewsets
from .serializers import productSerializer, employeeSerializer, ActiveUserSerializer
from .models import Product, Employee, ActiveUser
from uuid import uuid4
from random import randint

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


# Process all client requests made to the product listing page
def productListing(request, queryString='default', queryType='default'):

	# Require an active session to view the product listing page
	if (not request.session.session_key):
		return signIn(request, 'Register Error: You must sign-in to view the product listing page', 'error')

	# Render the product lising page
	return render(request, 'productListing.html',
				 {'products': Product.objects.all(), 
				 'queryString': queryString, 
				 'queryType': queryType})


# Process all client requests made to the product details page
def productDetails(request, productUUID, queryString='default', queryType='default'):

	# Require an active session to view the product details page
	if (not request.session.session_key):
		return signIn(request, 'Register Error: You must sign-in to view the product details page', 'error')

	# Render the product details page
	return render(request, 'productDetails.html', 
				 {'product': get_object_or_404(Product, productUUID=productUUID), 
				 'queryString': queryString,
				 'queryType': queryType})


# Process all client requests made to the product creation page
def productCreate(request, queryString='default', queryType='default'):

	# Require an active session to view the product creation page
	if (not request.session.session_key):
		return signIn(request, 'Register Error: You must sign-in to view the product creation page', 'error')

	# Render the product creation page
	return render(request, 'productCreate.html', 
				 {'queryString': queryString,
				 'queryType': queryType})


# Process all client requests made to the register menu page
def registerMenu(request, queryString='default', queryType='default'):

	# Require an active session to view the register menu page
	if (not request.session.session_key):
		return signIn(request, 'Register Error: You must sign-in to view the register menu page', 'error')

	# Render the register menu page
	return render(request, 'registerMenu.html', 
				 {'queryString': queryString,
				 'queryType': queryType})


# Process all client requests for page not found errors
def register_404(request, exception):
	return render(request, 'register_404.html')


# Process all client requests made to the employee details page
def employeeDetails(request, queryString='default', queryType='default'):

	# Always permit the request if there are no users in the database
	if (not Employee.objects.count()):
		return render(request, 'employeeDetails.html', 
					 {'queryString': 'databaseEmpty', 
					 'queryType': 'information'})

	# Require an active session to view the employee details page
	if (not request.session.session_key):
		return signIn(request, 'Register Error: You must sign-in to view the employee details page', 'error')

	# Process a request when an employeeID is passed in the URL
	if (str(queryString).isdigit() and int(queryString) > 0):
		return render(request, 'employeeDetails.html', 
					 {'employee': get_object_or_404(Employee, employeeID=int(queryString)), 
					 'employeeID': int(queryString),
					 'queryType': queryType})

	# Render the employee details page
	return render(request, 'employeeDetails.html', 
				 {'queryString': queryString, 
				 'queryType': queryType})


# Process all client requests made to the employee create view
def employeeCreate(request, queryString='default', queryType='default'):

	"""
	Only require an active session to access this view if there are
	one or more employees in the database. This will ensure that the
	very first employee will be able to create a new account without
	any issues. However, every attempt to create a new account after
	the very first employee will require an active session. We also
	perform some additional checks in the template to ensure only
	a manager can create a new account
	"""
	if (not request.session.session_key and Employee.objects.count()):
		return signIn(request, 'Register Error: You must sign-in to view the employee details page', 'error')

	# Listen for incoming POST requests
	if (request.method == "POST"):

		"""
		The provided documentation never explicitly said if the employeeID's
		are suppose to be randomly generated or not. However, I am going to
		assume they are randomly generated, because there is never a time
		when the employeeID field is editable by any person, even a manager.
		"""
		employeeID = randint(10000, 99999)

		# This value will only be true if there are no other employees in the database
		employeeInitial = False

		# Grab the rest of the data from the post request
		employeeFirstName = request.POST.get('employeeFirstName')
		employeeLastName = request.POST.get('employeeLastName')
		employeePassword = request.POST.get('employeePassword')
		employeeClassification = request.POST.get('employeeClassification')

		# Do not accept a blank last name
		if (employeeLastName == ' '):
			# The request failed. Return to the signIn page with an appropriate error message
			return employeeDetails(request, 'Register Error: The last name may not be blank', 'error')

		# Do not accept a blank password
		if (employeePassword == ' '):
			return employeeDetails(request, 'Register Error: The password may not be blank', 'error')

		# Process the special case when the initial employee is being created
		if (not Employee.objects.count()):
			employeeClassification = 2
			employeeInitial = True

		# This is an additional, paranoid check to avoid employeeID collisions
		if (Employee.objects.filter(employeeID=employeeID).exists()):
			employeeID = randint(10000, 99999)

		# Write the new employee record to the database
		Employee.objects.create(employeeID=employeeID,
								employeeFirstName=employeeFirstName,
								employeeLastName=employeeLastName,
								employeePassword=employeePassword,
								employeeClassification=employeeClassification)

		"""
		employeeInitial being true means that this was the very first
		employee being created. So, as per the instructions, we need
		to redirect them back to the sign-in page with the ID field
		automatically populated
		"""
		if (employeeInitial):
			return signIn(request, employeeID, 'redirect')

		"""
		employeeInitial being false means that this is not the very
		first employee being created. So, as per the instructions,
		we just need to redirect them to the newly created employee
		profile
		"""
		if (not employeeInitial):
			return employeeDetails(request, employeeID, 'successCreate')

	# Render the employee details page if an account is not being made
	return HttpResponseRedirect('/employeeDetails')


# Process all client requests made to the employee update view
def employeeUpdate(request, queryString='default', queryType='default'):

	# Require an active session to view the employee details page
	if (not request.session.session_key):
		return signIn(request, 'Register Error: You must sign-in to view the employee details page', 'error')

	# Listen for incoming POST requests
	if (request.method == "POST"):

		# Grab the rest of the data from the post request
		employeeID = request.POST.get('employeeID')
		employeeFirstName = request.POST.get('employeeFirstName')
		employeeLastName = request.POST.get('employeeLastName')
		employeePassword = request.POST.get('employeePassword')
		employeeClassification = request.POST.get('employeeClassification')

		"""
		The queryString and queryType are used in a weird way here
		because the errors have to be redirected back to a specific
		employee profile. So, I used the queryString to hold the
		employeeID and used the queryType to signal the type of
		error so I can just generate the appropriate response
		in the template.
		"""

		# Do not accept a blank first name
		if (employeeFirstName == ' '):
			return employeeDetails(request, employeeID, 'errorFirst')

		# Do not accept a blank last name
		if (employeeLastName == ' '):
			return employeeDetails(request, employeeID, "errorLast")

		# Do not accept a blank password
		if (employeePassword == ' '):
			return employeeDetails(request, employeeID, "errorPass")

		# Check if the provided employeeID maps to an existing user
		if (not Employee.objects.filter(employeeID=employeeID).exists()):
			return employeeDetails(request, employeeID, "employeeNoExist")


		# Update the employee database record
		Employee.objects.filter(employeeID=employeeID).update(employeeFirstName=employeeFirstName,
															  employeeLastName=employeeLastName,
															  employeePassword=employeePassword,
															  employeeClassification=employeeClassification)

		# Return to the employee profile with a success response
		return employeeDetails(request, employeeID, "successUpdate")

	# Render the employee details page if an account is not being updated
	return HttpResponseRedirect('/employeeDetails')


# Process all client requests made to the signIn page
def signIn(request, queryString='default', queryType='default'):

	"""
	When queryType is set to redirect this means we are being redirected here from
	the employee creatiion view and an initial employee has been created. So, we 
	need to pass the appropriate information to automatically populate the ID field
	"""
	if (str(queryString).isdigit() and queryType == "redirect"):
		return render(request, 'signin.html', 
					 {'employees': Employee.objects.all(), 
					 'employeeID': int(queryString), 
					 'queryType': queryType})

	# Listen for incoming POST requests
	if (request.method == 'POST'):

		# Grab the username and password from the signIn form
		employeeID = request.POST.get('employeeID')
		employeePassword = request.POST.get('employeePassword')

		# EmployeeID must be an integer
		if (not str(employeeID).isdigit()):
			queryString = 'Register Error: The employeeID must be a valid integer'
			return render(request, 'signin.html', 
						 {'employees': Employee.objects.all(), 
						 'queryString': queryString,
						 'queryType': 'error'})

		# Do not accept a blank employeeID
		if (employeeID == ' '):
			queryString = 'Register Error: The employeeID may not be blank'
			return render(request, 'signin.html', 
						 {'employees': Employee.objects.all(), 
						 'queryString': queryString,
						 'queryType': 'error'})

		# Do not accept a blank password
		if (employeePassword == ' '):
			queryString = 'Register Error: The password may not be blank'
			return render(request, 'signin.html', 
						 {'employees': Employee.objects.all(), 
						 'queryString': queryString,
						 'queryType': 'error'})

		# Check if an employee account with the provided employeeID and password exists
		employee = Employee.objects.filter(employeeID=employeeID)

		if (employee.exists()):

			# Get information about the user who just signed into the system
			activeEmployee = Employee.objects.get(employeeID=employeeID)

			# The employee exists and the provided password matches what is in the database
			if (employeePassword == activeEmployee.employeePassword):
				# Combine the FirstName and LastName into one variable to make the active name
				activeName = ('{} {}').format(str(activeEmployee.employeeFirstName), str(activeEmployee.employeeLastName))

				"""
				Attempting to use a Django session key as the activeSessionKey proved to be
				really unreliable. It caused all kinds of unexpected behavior because at
				seemingly random times, Django would return null for the session key
				and that would break everything because the database does not allow
				the activeSessionKey to be null. So, I am getting around this problem
				by generating a random activeSessionKey and passing it around as a 
				Django session variable. This is far more reliable and it still allows
				the register to use Django to track the employees session without
				any issues.
				"""
				activeSessionKey = uuid4().hex

				# Create a new session or update an existing session for the employee
				request.session.save()

				# Create session variables. These are used in the signOff function.
				request.session['employeeID'] = employeeID
				request.session['fullName'] = activeName
				request.session['employeeClassification'] = activeEmployee.employeeClassification
				request.session['activeKey'] = activeSessionKey

				# Check if the employee already has an ActiveUser database record
				activeSessionCheck = ActiveUser.objects.filter(activeEmployeeUUID=activeEmployee.employeeUUID)

				if (activeSessionCheck.exists()):
					# Update the employees ActiveUser session key
					ActiveUser.objects.filter(activeEmployeeUUID=activeEmployee.employeeUUID).update(activeSessionKey=activeSessionKey)
				else:
					# Create a new ActiveUser database record for the employee
					activeUser = ActiveUser.objects.create(activeEmployeeUUID=activeEmployee.employeeUUID,
															activeName=activeName,
															activeClassification=activeEmployee.employeeClassification,
															activeSessionKey=activeSessionKey)

				# Mark the employee as active
				Employee.objects.filter(employeeID=activeEmployee.employeeID).update(employeeActive=True)

				# The employee signed into the register. Redirect them to the main menu
				return registerMenu(request)
			else:
				# The request failed. Return to the signIn page with an appropriate error message
				queryString = 'Register Error: Bad employeeID or password'
				return render(request, 'signin.html', 
							 {'employees': Employee.objects.all(), 
						 	'queryString': queryString,
						 	'queryType': 'error'})
		else:
			# The request failed. Return to the signIn page with an appropriate error message
			queryString = 'Register Error: Bad employeeID or password'
			return render(request, 'signin.html', 
						 {'employees': Employee.objects.all(), 
						 'queryString': queryString,
						 'queryType': 'error'})

	# Render the sign-in page when no one is trying to sign into the register
	return render(request, 'signin.html', 
				 {'employees': Employee.objects.all(), 
				 'queryString': queryString,
				 'queryType': queryType})


# Process all client requests made to the signOff page
def signOff(request):

	# Disallowing access to the signOff view when there are no employees will prevent a KeyError from triggering
	if (not Employee.objects.count()):
		return HttpResponseRedirect('/signIn')

	# Only try to clean up if there is an active session
	if (request.session.session_key):

		if (request.session['activeKey']):
			# Delete the employee from the ActiveUsers database
			ActiveUser.objects.filter(activeSessionKey=request.session['activeKey']).delete()

		if (request.session['employeeID']):
			# Mark the employee as inactive
			Employee.objects.filter(employeeID=request.session['employeeID']).update(employeeActive=False)

		# Call Djangos built-in logout function to delete session information
		logout(request)

	# Redirect the user to the main page
	return HttpResponseRedirect('/signIn')
