"""
Helpful Resources:

	1. https://www.django-rest-framework.org/api-guide/serializers/
"""
from rest_framework import serializers
from .models import Product


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