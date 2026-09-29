from django.urls import path
from . import views

app_name = "order_tracker"

urlpatterns = [
    path('place/', views.place_order, name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
