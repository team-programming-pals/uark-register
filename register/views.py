from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product
import json

"""
See the following link for help with views
https://docs.djangoproject.com/en/3.1/topics/http/views/

Example

def Home(request):
    return render(request, 'home.html')
"""

def productAPI(request):
	if request.method == 'POST':
		post_data = json.loads(request.body)
		action = post_data['action']
		id = post_data['id']
		lookupcode = post_data['lookupcode']
		count = post_data['count']

		if action == "updateProduct":
			Product.updateProduct(id, lookupcode, count)
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=401)
			
	else:
		return HttpResponse(status=401)

def productListing(request):
    return render(request, 'productListing.html', {'products': Product.objects.all()})

def productDetail(request, id='no_uuid_specified'):
    if (id == 'no_uuid_specified'):
        return render(request, 'productDetail.html')
    else:
        return render(request, 'productDetail.html', {'product': get_object_or_404(Product, pk=id)})
