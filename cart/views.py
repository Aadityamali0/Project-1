from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from customer.models import Customer
from store.models import Product
from . models import Cart
from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required

# Create your views here.
def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    params = {
                'cart_products' : cart_items,
            }
    return render(request, 'cart/cart.html', params)

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
        
        cart_item = Cart.objects.create(
            user = user,
            name = name,
            phone_number = phone_number,
            quantity = quantity,
            product = product,
            image = product.image,
            price = product.price
            )
        print(cart_item.id)
        return redirect('cart:cart')
    
    return redirect('customer:login')

@require_POST
def delete_cart_item(request, id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(
            Cart,
            user=request.user,
            id=id
        )
        cart_item.delete()
    return redirect('cart:cart')

@require_POST
def updaate_quantity(request, id):
    if request.user.is_authenticated:
        quantity = int(request.POST.get('quantity'))
        cart_item = get_object_or_404(
            Cart,
            user = request.user,
            id = id
        )
        if quantity < 1:
            quantity = 1
        cart_item.quantity = quantity
        cart_item.save()
    return redirect ("cart:cart")