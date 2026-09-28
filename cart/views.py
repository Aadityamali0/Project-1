from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from customer.models import Customer
from store.models import Product
from . models import Cart
# from django.contrib.auth.decorators import login_required

# Create your views here.
def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        params = {
            'cart_products' : cart_items,
        }
        return render(request, 'cart/cart.html', params)

    return render(request, 'cart/cart.html')

# @login_required(login_url='customer:login')
def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        name = request.user.customer.name
        phone_number = request.user.customer.phone_number
        initial_quantity = request.POST.get('quantity')
        productid = request.POST.get('product_id') #prodyct id is stored here
        product =  get_object_or_404(Product, id=productid)
        
        quantity = int(initial_quantity) if initial_quantity else 1
        
        Cart.objects.create(
            user = user,
            name = name,
            phone_number = phone_number,
            quantity = quantity,
            product = product,
            image = product.image,
            price = product.price * quantity
            )
        return redirect('cart:cart')
    
    return redirect('customer:login')
