import re
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . models import Customer
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == "POST":
        fname = request.POST.get('fullname').strip()
        username = request.POST.get('username').strip()
        phone_number = request.POST.get('number').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if len(username) >= 20 or not re.match(r'^[A-Za-z0-9_]+$', username):
            messages.error(request, 'Username must have less than 15 characters (letters, numbers or underscore only).')
            return redirect('customer:register')

        if not phone_number.isdigit() or len(phone_number) != 10:
            messages.error(request, 'Enter a valid 10-digit phone number.')
            return redirect('customer:register')

        if password != confirm_password:
            messages.error(request, "Passwords don't match!")
            return redirect('customer:register')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return redirect('customer:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'That username is already taken. Create a new One.')
            return redirect('customer:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with that email already exists.')
            return redirect('customer:register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fname,
        )

        customer = Customer(
            user = user,
            name = fname,
            phone_number = phone_number
        )
        
        customer.register()
        
        messages.success(request, 'Account created successfully — you can sign in now.')
        # return redirect('customer:login')
        # return redirect('customer:login', messages.success('account created successfullly'))

    return render(request, 'customer/register.html')
    
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(username)
        print(bool(password))
        user = authenticate(
            request,
            username = username,
            password = password
        )
                
        if user is not None:
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('customer:login')
        
    return render(request, 'customer/login.html')
    
def user_logout(request):
    logout(request)
    return redirect('store:home')