from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    #functions when user clicks 'add to cart button'
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    #functions when user clicks 'cart' icon
    path('user-cart-details/', views.cart, name='cart'),
    path('delete/<int:id>/', views.delete_cart_item, name='delete_cart_item'),
    path('update/<int:id>/', views.update_quantity, name='update_quantity'),
]
