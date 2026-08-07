from django.shortcuts import render
from . models import Product

# Create your views here.
def index(request):
    product = Product.objects.all()
    params = {
        'swiper_product' : product
    }
    return render(request, 'store/index.html', params)