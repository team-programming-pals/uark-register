
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
	productPrice = models.FloatField(default=0.00)
	productCreationDate = models.DateTimeField(auto_now_add=True)

	def get_product_url(self):
		# Return a URL which can be used to display more information about a particular product
		return ('productDetails/{}').format(str(self.productUUID))
	
	def get_created_date(self):
		# Remove undesired information about the creation time of an item and only return the creation date
		return (datetime.strptime(str(self.productCreationDate).split()[0], '%Y-%m-%d').strftime('%m/%d/%Y'))

	def __str__(self):
		# This is the default response from a Product object
		return (str(self.productUUID))


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


"""
NOTE: These definitions will likely need to be re-worked for the next sprint.
	  I just added the definitions here to give myself a better idea of what
	  we are suppose to do.
"""

# Create a model for the transaction table in our database
class Transaction(models.Model):
	transactionUUID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	transactionCashierUUID = models.UUIDField(default='00000000-0000-0000-0000-000000000000', editable=False)
	transactionTotal = models.FloatField(default=0.00)
	transactionType = models.IntegerField(default=0)
	transactionReferenceID = models.UUIDField(default='00000000-0000-0000-0000-000000000000', editable=False)
	transactionCreationDate = models.DateTimeField(auto_now_add=True)

# Create a model for the transactionEntry table in our database
class transactionEntry(models.Model):
	transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='entry')
	entryUUID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
	productUUID = models.UUIDField(default='00000000-0000-0000-0000-000000000000', editable=False)
	entryQuantity = models.IntegerField(default=0)
	entryPrice = models.FloatField(default=0.00)
	entryCreationDate = models.DateTimeField(auto_now_add=True)