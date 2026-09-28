from . import views
from django.urls import path

app_name = 'store'

urlpatterns = [
    path('', views.index, name='home'),
    path('shop/', views.shop, name='shop'),
    path('contact/', views.contact, name='contact_us'),
    path('productdetails/<slug:slug>/<int:id>', views.productDetails, name='productDetails'),
]