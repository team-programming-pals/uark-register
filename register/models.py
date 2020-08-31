from django.db import models
from django.urls import reverse
from datetime import datetime
from uuid import uuid4

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    lookupcode = models.CharField(db_index=True, default='', max_length=32)
    count = models.IntegerField(default=0)
    createdon = models.DateTimeField(auto_now_add=True)

    def get_product_url(self):
        return ('productDetail/{}').format(str(self.id))
    
    def get_created_date(self):
        return (datetime.strptime(str(self.createdon).split()[0], '%Y-%m-%d').strftime('%m/%d/%Y'))

    def __str__(self):
        return (str(self.id))
