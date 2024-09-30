from django.shortcuts import render,redirect
from . models import Order,Ordered_item
from products.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from customers.models import Customer
# Create your views here.

def show_cart(request):
    user=request.user
    customer=user.customer_profile
    cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
                            )
    # Retrieve the cart items (Ordered_item) associated with the cart
    cart_items = Ordered_item.objects.filter(orders=cart_obj)

    context = {
        'cart': cart_obj,
        'cart_items': cart_items  # Pass the items to the template
    }

    return render(request, 'cart.html', context)

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
        user = request.user
        # Check if the customer profile exists, and create one if it doesn't
        if not hasattr(user, 'customer_profile'):
            customer = Customer.objects.create(user=user)
        else:
            customer = user.customer_profile
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')

        # Fetch or create the cart (Order) for the customer
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        # Fetch the product
        product = Product.objects.get(pk=product_id)

        # Add or update the Ordered_item
        Ordered_items, created = Ordered_item.objects.get_or_create(
            product=product,
            orders=cart_obj,  # Correct field name 'orders'
        )

        if created:
            Ordered_items.quantity = quantity
            
        else:
            Ordered_items.quantity += quantity
        Ordered_items.save()
        
        print(f"Saved Ordered Item: {Ordered_items.product.title}, Updated Quantity: {Ordered_items.quantity}")

        print(f"Added {Ordered_items.product.title} to the cart with quantity {Ordered_items.quantity}")
        print(f"Product ID: {product_id}, Quantity: {quantity}")
        print(f"Cart Object: {cart_obj}, Created: {created}")
        

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
    user = request.user

    # Check if the user has a customer profile before proceeding
    if hasattr(user, 'customer_profile'):
        customer = user.customer_profile
        all_orders = Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
        context = {'orders': all_orders}  # Changed 'order' to 'orders'
    else:
        # Handle the case where there's no customer profile
        context = {'orders': None}  # Changed 'order' to 'orders'

    return render(request, 'orders.html', context)

