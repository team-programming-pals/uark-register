"""
Helpful Resources:

	1. https://www.django-rest-framework.org/api-guide/serializers/
"""
from rest_framework import serializers
from rest_framework.response import Response
from .models import Product, Employee, ActiveUser
from random import randint

class productSerializer(serializers.HyperlinkedModelSerializer):
	"""
	Tell DRF a little more about our employee models so it will
	help us format the information correctly
	"""
	productCode = serializers.CharField(required=True)
	productCount = serializers.IntegerField(required=True)

	class Meta:
		model = Product
		fields = ('productUUID', 'productCode', 'productCount', 'productCreationDate')

class employeeSerializer(serializers.HyperlinkedModelSerializer):

	"""
	Tell DRF a little more about our employee model so it will
	help us format the information correctly. However, please
	note that I intentionally omitted the EmployeeID because
	users do not have direct access to this value without
	doing things that no normal user would ever do. Since
	we were told not to worry about security, I am only
	focusing on the beahvior under normal circumstances
	"""
	employeeFirstName = serializers.CharField(required=True)
	employeeLastName = serializers.CharField(required=True)
	employeePassword = serializers.CharField(required=True)
	employeeClassification = serializers.IntegerField(required=True)

	class Meta:
		model = Employee
		fields = ('employeeUUID', 'employeeID', 'employeeFirstName', 'employeeLastName',
					'employeePassword', 'employeeActive', 'employeeClassification',
					'employeeeManagerUUID', 'employeeCreationDate')

class ActiveUserSerializer(serializers.HyperlinkedModelSerializer):

	"""
	Tell DRF a little more about our active user model so it will
	help us format the information correctly
	"""
	activeName = serializers.CharField(required=True)
	activeClassification = serializers.IntegerField(required=True)
	activeSessionKey = serializers.CharField(required=True)

	class Meta:
		model = ActiveUser
		fields = ('activeUUID', 'activeEmployeeUUID', 'activeName', 'activeClassification',
					'activeSessionKey', 'activeCreationDate')


class transactionSerializer(serializers.HyperlinkedModelSerializer):

	"""
	Tell DRF a little more about our active user model so it will
	help us format the information correctly
	"""
	activeName = serializers.CharField(required=True)
	activeClassification = serializers.IntegerField(required=True)
	activeSessionKey = serializers.CharField(required=True)

	class Meta:
		model = ActiveUser
		fields = ('activeUUID', 'activeEmployeeUUID', 'activeName', 'activeClassification',
					'activeSessionKey', 'activeCreationDate')