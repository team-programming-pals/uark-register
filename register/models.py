
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
