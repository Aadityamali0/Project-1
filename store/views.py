from django.shortcuts import render
from . models import Product, Category

# Create your views here.
def index(request):
    product = Product.objects.all()
    params = {
        'swiper_product' : product
    }
    return render(request, 'store/index.html', params)

def shop(request):
    categories = Category.objects.all()
    
    categoryID = request.GET.get('category')
    
    if categoryID:
        products = Product.objects.filter(category=categoryID)
    else:
        products = Product.objects.all()
        
    params = {
        'products' : products,
        'category' : categories
    }
    return render (request, 'store/shop.html', params)