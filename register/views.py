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
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import productSerializer, employeeSerializer, ActiveUserSerializer
from .models import Product, Employee, ActiveUser, Transaction, shoppingCart, shoppingCartItems
from uuid import uuid4
from random import randint



"""
These view sets are not required for the register to function,
but making our models publicly accessible through DRF will make
testing new features much easier. Additionally, I will share a
link to these publicly exposed views so the graders can use them
to verify that the register is working correctly
"""
class productViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = productSerializer

class employeeViewSet(viewsets.ModelViewSet):
	queryset = Employee.objects.all()
	serializer_class = employeeSerializer

class activeUserViewSet(viewsets.ModelViewSet):
	queryset = ActiveUser.objects.all()
	serializer_class = ActiveUserSerializer

"""
manageProducts is a class-based view which is used as a
central maangement interface for all Product-related actions
"""
class manageProducts(APIView):
	def post(self, request, format=None):
		serializer = productSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'queryResponse': 'The product was successfully added'}, status=status.HTTP_201_CREATED)

		"""
		These if statements were the easiest way I could find
		to send custom error responses from the API end-point
		"""
		if (str(serializer.data['productCode']).strip() == ''):
			return Response({'queryResponse': 'The product name field may not be left blank'}, status=status.HTTP_400_BAD_REQUEST)

		if (str(serializer.data['productCount']).strip() == ''):
			return Response({'queryResponse': 'The product quantity field may not be left blank'}, status=status.HTTP_400_BAD_REQUEST)

		if (not str(serializer.data['productCount']).isdigit()):
			return Response({'queryResponse': 'The product quantity field must be a valid integer'}, status=status.HTTP_400_BAD_REQUEST)

		# There is some input validation problem I did not check for
		return Response({'queryResponse': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, productUUID, format=None):
		product = Product.objects.get(productUUID=productUUID)
		serializer = productSerializer(product, data=request.data)
		if serializer.is_valid():
			if (not Product.objects.filter(productUUID=productUUID).exists()):
				return Response({'queryResponse': 'The product you are trying to delete does not exist'}, status=status.HTTP_400_BAD_REQUEST)

			if (request.session['employeeClassification'] > 0):
				serializer.save()
				return Response({'queryResponse': 'The product record was successfully updated'}, status=status.HTTP_201_CREATED)
			else:
				return Response({'queryResponse': 'You must be a manager to update product records'}, status=status.HTTP_400_BAD_REQUEST)

		"""
		These if statements were the easiest way I could find
		to send custom error responses from the API end-point
		"""
		if (str(serializer.data['productCode']).strip() == ''):
			return Response({'queryResponse': 'The product name field may not be left blank'}, status=status.HTTP_400_BAD_REQUEST)

		if (str(serializer.data['productCount']).strip() == ''):
			return Response({'queryResponse': 'The product quantity field may not be left blank'}, status=status.HTTP_400_BAD_REQUEST)

		if (not str(serializer.data['productCount']).isdigit()):
			return Response({'queryResponse': 'The product quantity field must be a valid integer'}, status=status.HTTP_400_BAD_REQUEST)

		# There is some input validation problem I did not check for
		return Response({'queryResponse': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, productUUID, format=None):
		if (not Product.objects.filter(productUUID=productUUID).exists()):
			return Response({'queryResponse': 'The product you are trying to delete does not exist'}, status=status.HTTP_400_BAD_REQUEST)

		if (request.session['employeeClassification'] > 0):
			Product.objects.filter(productUUID=productUUID).delete()
			return Response({'queryResponse': 'The product record was successfully deleted'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'queryResponse': 'You must be a manager to delete product records'}, status=status.HTTP_400_BAD_REQUEST)

		# There is some input validation problem I did not check for
		return Response({'queryResponse': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

"""
manageEmployees is a class-based view which is used as a
central management interface for all Employee-related actions
"""
class manageEmployees(APIView):
	def post(self, request, format=None):
		serializer = employeeSerializer(data=request.data)
		if serializer.is_valid():
			employeeID = randint(10000, 99999)
			if (not Employee.objects.count()):
				serializer.save(employeeID=employeeID, employeeClassification = 2)
				return Response({'queryResponse': 'initial', 'employeeID': int(serializer.data['employeeID'])}, status=status.HTTP_201_CREATED)
			else:
				serializer.save(employeeID=employeeID)
				return Response({'queryResponse': 'The employee account was successfully created', 'employeeID': int(serializer.data['employeeID'])}, status=status.HTTP_201_CREATED)

		"""
		These if statements were the easiest way I could find
		to send custom error responses from the API end-point
		"""
		if (str(serializer.data['employeeFirstName']).strip() == ''):
			return Response({'queryResponse': 'The first name field may not be left blank'}, status=status.HTTP_400_BAD_REQUEST)

		if (str(serializer.data['employeeLastName']).strip() == ''):
			return Response({'queryResponse': 'The last name field may not be left blank'}, status=status.HTTP_400_BAD_REQUEST)

		if (str(serializer.data['employeePassword']).strip() == ''):
			return Response({'queryResponse': 'The password field may not be left blank'}, status=status.HTTP_400_BAD_REQUEST)

		if (str(serializer.data['employeeClassification']).strip() == ''):
			return Response({'queryResponse': 'You must select an employee type'}, status=status.HTTP_400_BAD_REQUEST)

		# There is some input validation problem I did not check for
		return Response({'queryResponse': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


	def put(self, request, employeeUUID, format=None):
		employee = Employee.objects.get(employeeUUID=employeeUUID)
		serializer = employeeSerializer(employee, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'queryResponse': 'The employee record was successfully updated'}, status=status.HTTP_201_CREATED)

		"""
		These if statements were the easiest way I could find
		to send custom error responses from the API end-point
		"""
		if (str(serializer.data['employeeFirstName']).strip() == ''):
			return Response({'queryResponse': 'The first name field may not be left blank'}, status=status.HTTP_400_BAD_REQUEST)

		if (str(serializer.data['employeeLastName']).strip() == ''):
			return Response({'queryResponse': 'The last name field may not be left blank'}, status=status.HTTP_400_BAD_REQUEST)

		if (str(serializer.data['employeePassword']).strip() == ''):
			return Response({'queryResponse': 'The password field may not be left blank'}, status=status.HTTP_400_BAD_REQUEST)

		if (str(serializer.data['employeeClassification']).strip() == ''):
			return Response({'queryResponse': 'You must select an employee type'}, status=status.HTTP_400_BAD_REQUEST)

		# There is some input validation problem I did not check for
		return Response({'queryResponse': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# Process all client requests made to the product listing page
def productListing(request, queryString=None):

	# Require an active session to view the product listing page
	if (not request.session.session_key or not Employee.objects.count()):
		return redirect('signIn', queryString='You must be signed into the register to view the product listing page')

	# Grab the relevant employee and product from their respective tables	
	employee = Employee.objects.get(employeeID=request.session['employeeID'])
	cartTest = shoppingCart.objects.filter(employee=employee)

	# Render the product lising page
	return render(request, 'productListing.html',
				 {'products': Product.objects.all(), 
				 'queryString': queryString, 'cart': cartTest})


# Process all client requests made to the product details page
def productDetails(request, productUUID, queryString=None):

	# Require an active session to view the product details page
	if (not request.session.session_key or not Employee.objects.count()):
		return redirect('signIn', queryString='You must be signed into the register to view the product details page')

	# Grab the relevant employee and product from their respective tables	
	employee = Employee.objects.get(employeeID=request.session['employeeID'])
	cartTest = shoppingCart.objects.filter(employee=employee)

	# Render the product details page
	return render(request, 'productDetails.html', 
				 {'product': get_object_or_404(Product, productUUID=productUUID), 
				 'queryString': queryString,
				 'cart': cartTest})


# Process all client requests made to the product creation page
def productCreate(request, queryString=None):

	# Require an active session to view the product creation page
	if (not request.session.session_key or not Employee.objects.count()):
		return redirect('signIn', queryString='You must be signed into the register to view the create product page')

	# Render the product creation page
	return render(request, 'productCreate.html', 
				 {'queryString': queryString})


# Process all client requests made to the register menu page
def registerMenu(request, queryString=None):

	# Require an active session to view the register menu page
	if (not request.session.session_key or not Employee.objects.count()):
		return redirect('signIn', queryString='You must be signed into the register to view the register menu page')

	# Grab the relevant employee and product from their respective tables	
	employee = Employee.objects.get(employeeID=request.session['employeeID'])
	cartTest = shoppingCart.objects.filter(employee=employee)
	# Render the register menu page
	return render(request, 'registerMenu.html', 
				 {'queryString': queryString,'cart': cartTest})


# Process all client requests for page not found errors
def register_404(request, exception):
	return render(request, 'register_404.html')


# Process all client requests made to the employee details page
def employeeDetails(request, queryString=None, employeeID=None):
	# Grab the relevant employee and product from their respective tables	
	employee = Employee.objects.get(employeeID=request.session['employeeID'])
	cartTest = shoppingCart.objects.filter(employee=employee)

	# Always permit the request if there are no users in the database
	if (not Employee.objects.count()):
		return render(request, 'employeeDetails.html', 
					 {'database': 'empty'})

	# Require an active session to view the employee details page
	if (not request.session.session_key):
		return redirect('signIn', queryString='You must be signed into the register to view the employee details page')

	# Process a request when an employeeID is passed in the URL
	if (employeeID):
		
		return render(request, 'employeeDetails.html', 
					 {'employee': get_object_or_404(Employee, employeeID=employeeID), 
					 'employeeID': employeeID,
					 'cart': cartTest})

	# Render the employee details page
	return render(request, 'employeeDetails.html',
				 {'queryString': queryString,
				 "cart": cartTest})


# Process all client requests made to the signIn page
def signIn(request, employeeID=None, queryString=None):

	# Listen for incoming POST requests
	if (request.method == 'POST'):

		# Grab the username and password from the signIn form
		employeeID = request.POST.get('employeeID')
		employeePassword = request.POST.get('employeePassword')

		# EmployeeID must be an integer
		if (not str(employeeID).isdigit()):
			return render(request, 'signin.html', 
						 {'employees': Employee.objects.all(), 
						 'queryString': queryString,
						 'queryType': 'errorEmployeeInt'})

		# Do not accept a blank employeeID
		if (str(employeeID).strip() == ''):
			return render(request, 'signin.html', 
						 {'employees': Employee.objects.all(), 
						 'queryString': queryString,
						 'queryType': 'errorEmployeeID'})

		# Do not accept a blank password
		if (str(employeePassword).strip() == ''):
			return render(request, 'signin.html', 
						 {'employees': Employee.objects.all(), 
						 'queryString': queryString,
						 'queryType': 'errorPassword'})

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
					# Update the employees ActiveUser session
					ActiveUser.objects.filter(activeEmployeeUUID=activeEmployee.employeeUUID).update(activeEmployeeUUID=activeEmployee.employeeUUID,
																									 activeName=activeName,
											  														 activeClassification=activeEmployee.employeeClassification, 
											  														 activeSessionKey=activeSessionKey)
				else:
					# Create a new ActiveUser database record for the employee
					activeUser = ActiveUser.objects.create(activeEmployeeUUID=activeEmployee.employeeUUID,
															activeName=activeName,
															activeClassification=activeEmployee.employeeClassification,
															activeSessionKey=activeSessionKey)

				# Mark the employee as active
				Employee.objects.filter(employeeID=activeEmployee.employeeID).update(employeeActive=True)

				# The employee signed into the register. Redirect them to the main menu
				return redirect('registerMenu')
			else:
				# The request failed. Return to the signIn page with an appropriate error message
				return redirect('signIn', queryString='Bad EmployeeID or password')
		else:
			# The request failed. Return to the signIn page with an appropriate error message
			return redirect('signIn', queryString='Bad EmployeeID or password')

	if (employeeID):
		return render(request, 'signin.html', 
					 {'employees': Employee.objects.all(), 
					 'employeeID': employeeID})

	# Render the sign-in page when no one is trying to sign into the register
	return render(request, 'signin.html', 
				 {'employees': Employee.objects.all(), 
				 'queryString': queryString})


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

# Process all client requests to the transaction page
def transactionMenu(request, queryString=None):
	# Require an active session to view the transaction page
	if (not request.session.session_key or not Employee.objects.count()):
		return redirect('signIn', queryString='You must be signed into the register to view the transaction page')
	
	# Grab the current employees shopping cart (This is only here for testing)
	employee = Employee.objects.get(employeeID=request.session['employeeID'])
	cartTest = shoppingCart.objects.filter(employee=employee)

	# This block of code will handle the search feature. I will probably clean this up and improve it later
	if (request.method == 'GET'):
		query = request.GET.get('query')
		if (query):
			# Return the search results
			foundProducts = Product.objects.filter(productCode__icontains=query)
			employeeUUID = Employee.objects.values_list('employeeUUID', flat=True).get(employeeID=request.session['employeeID'])
			return render (request, 'transaction.html', {'products': foundProducts, 'employeeUUID': employeeUUID, 'cart': cartTest, 'queryString': queryString })
		else:
			return render (request, 'transaction.html', {'cart': cartTest, 'queryString': queryString})
	
# Process all client requests to the transaction details page
def transactionDetails(request):
	# Require an active session to view the transaction details page
	if (not request.session.session_key or not Employee.objects.count()):
		return redirect('signIn', queryString='You must be signed into the register to view the transaction details page')

	# Grab the current employees shopping cart
	employee = Employee.objects.get(employeeID=request.session['employeeID'])
	cartTest = shoppingCart.objects.filter(employee=employee)

	return render(request, 'transactionDetails.html', {'cart': cartTest})

# Add items to a shopping cart
def addCartItem(request):
	# TODO: Restrict this to logged in employees only
	if (request.method == 'POST'):
		employeeUUID = request.POST.get('employeeUUID')
		productUUID = request.POST.get('productUUID')

		# Grab the relevant employee and product from their respective tables
		employee = Employee.objects.get(employeeUUID=employeeUUID)
		product = Product.objects.get(productUUID=productUUID)

		# Create a new cart item or update the quantity of an existing cart item
		if (shoppingCartItems.objects.filter(product=product).exists()):
			# Update quantity for an item
			newQuantity = int(shoppingCartItems.objects.get(product=product).quantity) + 1
			shoppingCartItems.objects.filter(product=product).update(quantity=newQuantity)
			return redirect('transactionMenu', queryString='Item added to cart!')
		else:
			# Create a new iem
			cartItem = shoppingCartItems.objects.create(product=product, quantity=1)
			employeeCart = shoppingCart.objects.get_or_create(employee=employee)
			employeeCart[0].products.add(cartItem)
			employeeCart[0].save()
			return redirect('transactionMenu', queryString='Item added to cart!')
	
	return redirect('transactionMenu')


# Delete items from a shopping cart
def deleteCartItem(request):
	# TODO: Restrict this to logged in employees only
	if (request.method == 'POST'):
		productUUID = request.POST.get('productUUID')
		product = Product.objects.get(productUUID=productUUID)

		if (int(shoppingCartItems.objects.get(product=product).quantity) > 1):
			# Remove one of the quantities
			newQuantity = int(shoppingCartItems.objects.get(product=product).quantity) - 1
			shoppingCartItems.objects.filter(product=product).update(quantity=newQuantity)
			return redirect('transactionMenu')
		else:
			# Delete the product
			shoppingCartItems.objects.filter(product=product).delete()
			return redirect('transactionMenu')
	
	return redirect('transactionMenu')


# Update the quantity of items in a shopping cart
def updateCartQuantity(request):
	# TODO: Restrict this to logged in employees only
	if (request.method == 'POST'):
		productUUID = request.POST.get('productUUID')
		productQuantity = request.POST.get('quantity')

		product = Product.objects.get(productUUID=productUUID)

		if (int(productQuantity) > 0):
			# Update the quantity 
			shoppingCartItems.objects.filter(product=product).update(quantity=productQuantity)
			return redirect('transactionMenu')
		else:
			# Delete the product if they enter zero quantities or less
			shoppingCartItems.objects.filter(product=product).delete()
			return redirect('transactionMenu')
	
	return redirect('transactionMenu')