from django.shortcuts import render,redirect
from django.urls import reverse
from . models import Product
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    featured_products=Product.objects.order_by('priority')[:3]
    latest_products=Product.objects.order_by('-id')[:3]
    context={
        'featured_products':featured_products,
        'latest_products':latest_products
    }
    
    return render(request,'index.html',context)


def products(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    product_list=Product.objects.order_by('priority')
    product_paginator=Paginator(product_list,2)
    product_list=product_paginator.get_page(page)
    # product_ids = [product for product in product_list]
    
    context={'products':product_list}
    # for product in product_ids:
    #     print("*"*50)
    #     print(product.id)
    #     print("*"*50)
    return render (request,'products.html',context)


def product_details(request,id):
    product=Product.objects.get(id=id)
    context={'product':product}
    return render(request,'product_details.html',context)
    # product_id = 1
    # return redirect('product_details', kwargs={'id': product_id}))