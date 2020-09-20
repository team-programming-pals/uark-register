from django.db import models
from django.urls import reverse
from datetime import datetime
from uuid import uuid4

"""
Django uses models to define the data we are working with. Each of our models will map
to a single database table. We can also expand on the model to add useful abstractions
which allow us to manipulate the data in meaningful ways.

See the following link for more information
https://docs.djangoproject.com/en/3.1/topics/db/models/
"""
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    lookupcode = models.CharField(db_index=True, default='', max_length=32)
    count = models.IntegerField(default=0)
    createdon = models.DateTimeField(auto_now_add=True)

    def get_product_url(self):
        # Return a URL which can be used to display more information about a particular product
        return ('productDetail/{}').format(str(self.id))
    
    def get_created_date(self):
        # Remove undesired information about the creation time of an item and only return the creation date
        return (datetime.strptime(str(self.createdon).split()[0], '%Y-%m-%d').strftime('%m/%d/%Y'))

    def updateProduct(id, lookupcode, count):
        # Create a new object that references a specific database entry
        updateObject = Product.objects.get(pk=id)

        # Update the lookupcode and count values
        updateObject.lookupcode = lookupcode
        updateObject.count = count

        # Save our changes to the database
        updateObject.save()

        return (str("SUCCESS"))

    def __str__(self):
        # This is the default response from a Product object
        return (str(self.id))
