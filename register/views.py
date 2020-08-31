from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product

def productListing(request):
    return render(request, 'productListing.html', {'products': Product.objects.all()})

def productDetail(request, id='no_uuid_specified'):
    if (id == 'no_uuid_specified'):
        return render(request, 'productDetail.html')
    else:
        return render(request, 'productDetail.html', {'product': get_object_or_404(Product, pk=id)})

def productCreate(request):
    return render(request, 'productCreate.html')