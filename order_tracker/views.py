from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from cart.models import Cart
from .models import Order, OrderItem


@require_POST
def place_order(request):
    """Turns the logged-in user's cart into an Order and empties the cart."""
    if not request.user.is_authenticated:
        return redirect('customer:login')

    cart_items = list(Cart.objects.filter(user=request.user).select_related('product'))
    if not cart_items:
        return redirect('cart:cart')

    try:
        customer = request.user.customer
        name, phone_number = customer.name, customer.phone_number
    except ObjectDoesNotExist:
        name, phone_number = request.user.get_full_name() or request.user.username, ''

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            name=name,
            phone_number=phone_number,
        )
        total = 0
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.product_name,
                quantity=item.quantity,
                price=item.price,
            )
            total += item.price * item.quantity
        order.total_price = total
        order.save(update_fields=['total_price'])
        Cart.objects.filter(id__in=[item.id for item in cart_items]).delete()

    return redirect('order_tracker:my_orders')


def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('customer:login')
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'order/order.html', {'orders': orders})

