from django.shortcuts import render,redirect
from . models import Order,Ordered_item
from products.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def show_cart(request):
    user=request.user
    customer=user.customer_profile
    cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
                            )
    context={'cart':cart_obj}
    return render(request,'cart.html',context)

def checkout_cart(request):
    try:
        if request.POST:
            user=request.user
            customer=user.customer_profile
            total=float(request.POST.get('total'))
            
            order_obj=Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
                                )
            if order_obj:
                order_obj.order_status=Order.ORDER_CONFIRMED
                order_obj.total_price=total
                order_obj.save()
                status_msg="your order proccessed"
                messages.success(request,status_msg)
            else:
                error_message="order not proccessed"
                messages.error(request,error_message)
    except Exception as e:
        error_message="order not proccessed"
        messages.error(request,error_message)
    return redirect ('cart')
@login_required(login_url='account')
def add_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=int(request.POST.get('quantity'))
        product_id=request.POST.get('product_id')
        cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
                            )
        product=Product.objects.get(pk=product_id)
        Ordered_items,created=Ordered_item.objects.get_or_create(
            product=product_id,
            owner=cart_obj,
            
        )
        if created:
            Ordered_items.quantity=quantity
            Ordered_items.save()
        else:
            Ordered_items.quantity=Ordered_items.quantity+quantity
            Ordered_items.save()
        return redirect('cart')
def remove_items(request,pk):

    item=Ordered_item.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect ('cart')
@login_required(login_url='account')
def view_orders(request):
    user=request.user
    customer=user.customer_profile
    
    
    return render(request,'cart.html')
@login_required(login_url='account')
def show_orders(request):
    user=request.user
    customer=user.customer_profile
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'order':all_orders}
    return render(request,'orders.html',context)