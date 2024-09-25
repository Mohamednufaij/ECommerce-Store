from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from . models import Customer
# Create your views here.
def sign_out(request):
    logout(request)
    return redirect('index')
def account(request):
    context = {}

    # Check if the form submitted is for registration
    if request.POST and 'register' in request.POST:
        context['register'] = True
        try:
            # Fetch registration details from POST
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')

            # Debugging output to check form data
            print('*' * 100)
            print(username, password, email, address, phone)
            print('*' * 100)

            # Create user account
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            # Create customer account
            customer = Customer.objects.create(
                name=username,
                user=user,
                phone=phone,
                address=address
            )

            # Success message for registration
            success_message = "User registered"
            messages.success(request, success_message)

        except Exception as e:
            # Error handling for duplicate username or invalid inputs
            error_message = "Duplicate username or invalid inputs"
            messages.error(request, error_message)

    # Check if the form submitted is for login
    elif request.POST and 'login' in request.POST:
        context['register'] = False
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('cart')
        else:
            error_message = "Invalid credentials"
            messages.error(request, error_message)

    return render(request, 'account.html', context)
