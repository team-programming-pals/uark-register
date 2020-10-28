
"""
Helpful Resources:

	1. https://docs.djangoproject.com/en/3.1/topics/db/models/
"""
from django.db import models
from django.urls import reverse
from datetime import datetime
from uuid import uuid4


# Create a model for the Product table in our database
class Product(models.Model):
	productUUID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	productCode = models.CharField(db_index=True, default='', max_length=32)
	productCount = models.IntegerField(default=0)
	productPrice = models.DecimalField(max_digits=200,decimal_places=2)
	productCreationDate = models.DateTimeField(auto_now_add=True)

	def get_product_url(self):
		# Return a URL which can be used to display more information about a particular product
		return ('productDetails/{}').format(str(self.productUUID))
	
	def get_created_date(self):
		# Remove undesired information about the creation time of an item and only return the creation date
		return (datetime.strptime(str(self.productCreationDate).split()[0], '%Y-%m-%d').strftime('%m/%d/%Y'))

	def __str__(self):
		# This is the default response from a Product object
		return (str(self.productCode))


# Create a model for the employees table in our database
class Employee(models.Model):
	employeeUUID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	employeeID = models.IntegerField(db_index=True, default=0)
	employeeFirstName = models.CharField(default='', max_length=128)
	employeeLastName = models.CharField(default='', max_length=128)
	employeePassword = models.CharField(default='', max_length=128)
	employeeActive = models.BooleanField(default=False)
	employeeClassification = models.IntegerField(default=0)
	employeeeManagerUUID = models.UUIDField(default='00000000-0000-0000-0000-000000000000', editable=False)
	employeeCreationDate = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		# This is the default response from a Employee object
		return (str(self.employeeID))


# Create a model for the activeuser table in our database
class ActiveUser(models.Model):
	activeUUID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	activeEmployeeUUID= models.UUIDField(db_index=True)
	activeName = models.CharField(default='', max_length=256)
	activeClassification = models.IntegerField(default=0)
	activeSessionKey = models.CharField(db_index=True, default='', max_length=128)
	activeCreationDate = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		# This is the default response from an ActiveUser object
		return (str(self.activeName))

# Create a model for the transaction table in our database
class Transaction(models.Model):
	transactionEmployee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
	transactionUUID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	transactionTotal = models.DecimalField(max_digits=200,decimal_places=2)
	transactionType = models.IntegerField(default=0)
	transactionReferenceID = models.UUIDField(default='00000000-0000-0000-0000-000000000000', editable=False)
	transactionCreationDate = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		# This is the default response from a Transaction object
		return (str(self.transactionCreationDate))

# Create a model for the shoppingCartItems table in our database
class shoppingCartItems(models.Model):
	product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(default=0)
	itemAddedDate = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		# This is the default response from a shoppingCartItems object
		return (str(self.product))


# Create a model for the shoppingCart table in our database
class shoppingCart(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
	cartUUID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	products = models.ManyToManyField(shoppingCartItems)
	cartCreationDate = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		# This is the default response from a shoppingCart object
		return (str(self.employee))

	def cart_total(self):
		# Return the sum of every product in the cart multiplied by its quantity
		return sum([(product.product.productPrice * product.quantity) for product in self.products.all()])