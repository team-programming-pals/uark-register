"""
Helpful Resources:

	1. https://www.django-rest-framework.org/api-guide/serializers/
"""
from rest_framework import serializers
from .models import Product, Employee, ActiveUser
import hashlib


# Create a serializer for our product API endpoint
class productSerializer(serializers.HyperlinkedModelSerializer):
	"""
	A serializer will convert our database queries and models into
	native Python datatypes that can be easily rendered into  a
	format like JSON
	"""
	class Meta:
		model = Product
		fields = ('productUUID', 'productCode', 'productCount', 'productCreationDate')


# Create a serializer for our Employee API endpoint
class employeeSerializer(serializers.HyperlinkedModelSerializer):
	"""
	A serializer will convert our database queries and models into
	native Python datatypes that can be easily rendered into  a
	format like JSON
	"""

	# Override the default create employee method so we can hash the password
	def create(self, validated_data):
		hashedEmployeePassword = hashlib.sha256(validated_data['employeePassword'].encode('utf-8')).hexdigest()
		createEmployee = Employee.objects.create(employeeID=validated_data['employeeID'],
												employeeFirstName=validated_data['employeeFirstName'],
												employeeLastName=validated_data['employeeLastName'],
												employeePassword=hashedEmployeePassword,
												employeeActive=validated_data['employeeActive'],
												employeeClassification=validated_data['employeeClassification'],)

		return createEmployee



	# Override the default update employee method so we can hash the password
	def update(self, validated_data):
		hashedEmployeePassword = hashlib.sha256(validated_data['employeePassword'].encode('utf-8')).hexdigest()
		createEmployee = Employee.objects.create(employeeID=validated_data['employeeID'],
												employeeFirstName=validated_data['employeeFirstName'],
												employeeLastName=validated_data['employeeLastName'],
												employeePassword=hashedEmployeePassword,
												employeeActive=validated_data['employeeActive'],
												employeeClassification=validated_data['employeeClassification'],)

		return updateEmployee



	class Meta:
		model = Employee
		fields = ('employeeUUID', 'employeeID', 'employeeFirstName', 'employeeLastName',
					'employeePassword', 'employeeActive', 'employeeClassification',
					'employeeeManagerUUID', 'employeeCreationDate')



# Create a serializer for our active users API endpoint
class ActiveUserSerializer(serializers.HyperlinkedModelSerializer):
	"""
	A serializer will convert our database queries and models into
	native Python datatypes that can be easily rendered into  a
	format like JSON
	"""
	class Meta:
		model = ActiveUser
		fields = ('activeUUID', 'activeEmployeeUUID', 'activeName', 'activeClassification',
					'activeSessionKey', 'activeCreationDate')