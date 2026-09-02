from django.shortcuts import render, get_object_or_404
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
    
    # gets the value of category which is passed from the url
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

def productDetails(request, id, slug):
    products = get_object_or_404(Product, id=id)
    
    related_products = Product.objects.filter(
        category = products.category
    ).exclude(id=products.id).order_by('?') [:10]
    
    params = {
        'related_products' : related_products,
        'subimages' : products.sub_images.all(),
        'products' : products,
    }
    
    return render(request, 'store/productDetailsPage.html', params)