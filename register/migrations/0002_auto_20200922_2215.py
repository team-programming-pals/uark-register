"""
Helpful Resources:

    1. https://docs.djangoproject.com/en/3.1/topics/migrations/
"""
from django.db import migrations


# Populate the products table with some initial data
def createTestValues(apps, schema_editor):
	# Access the registers Product model
	Product = apps.get_model('register', 'Product')

	# Create the 1st test value
	testValue = Product(productCode='ExampleItem1', productCount=25, productPrice=10.00)
	testValue.save()

	# Create the 2nd test value
	testValue = Product(productCode='ExampleItem2', productCount=50, productPrice=20.00)
	testValue.save()

	# Create the 3rd test value
	testValue = Product(productCode='ExampleItem3', productCount=75, productPrice=30.00)
	testValue.save()

	# Create the 4th test value
	testValue = Product(productCode='ExampleItem4', productCount=100, productPrice=40.00)
	testValue.save()

	# Create the 5th test value
	testValue = Product(productCode='ExampleItem5', productCount=125, productPrice=50.00)
	testValue.save()


# Run the second step of the migration process
class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(createTestValues),
    ]