from rest_framework import serializers
from .models import Product

class productSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Product
		fields = ('productUUID', 'productCode', 'productCount', 'productCreationDate')