from django.shortcuts import render, get_object_or_404
from . models import Product, Category
from django.core.paginator import Paginator

def index(request):
    product = Product.objects.all().order_by('?')
    params = {
        'swiper_product' : product
    }
    return render(request, 'store/index.html', params)

# def shop(request):
#     categories = Category.objects.all()
    
#     # gets the value of category which is passed from the url
#     categoryID = request.GET.get('category')
    
#     if categoryID:
#         products = Product.objects.filter(category=categoryID)
#     else:
#         products = Product.objects.all()
        
#     params = {
#         'products' : products,
#         'category' : categories
#     }
#     return render (request, 'store/shop.html', params)

def contact(request):
    return render(request, 'store/contact.html')
    
def shop(request):
    categories = Category.objects.all()
    
    categoryID =  request.GET.get('category')
    
    if categoryID:
        product_obj = Product.objects.filter(category=categoryID).order_by('?')
    else:
        product_obj = Product.objects.all().order_by('?')
    
    paginator = Paginator(product_obj,8)
    
    page_number = request.GET.get('page')
    
    product_obj = paginator.get_page(page_number)
    
    
    params = {
        'category' : categories,
        'product_obj' : product_obj,
    }
    return render(request, 'store/shop.html', params)


def productDetails(request, id, slug):
    # use slug when both id and slug should match in order to show the product details page
    # products = get_object_or_404(Product, id=id, slug=slug)
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
