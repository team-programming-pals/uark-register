"""programmingpals URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

Simplified instructions
    1. Add a URL to urlpatterns like I have done below
    2. Modify register/views.py and add support for the new URL
    3. Create a new HTML file for the URL in register/templates
    4. ???
    5. Profit
"""
from django.contrib import admin
from django.urls import path
from register import views

urlpatterns = [
    path('', views.productListing, name='productListing'),
    path('api/product/', views.productAPI, name='productAPI'),
    path('productDetail/<uuid:id>/', views.productDetail, name='productDetail'),
    path('productDetail/', views.productDetail, name='productDetail'),
    path('admin/', admin.site.urls),
]
