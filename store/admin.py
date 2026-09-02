from django.contrib import admin
from . models import Product, Category, SubImages

# Register your models here.
class SubImages(admin.TabularInline):
    model = SubImages
    extra = 4
    
class AdminProduct(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'category', 'price']
    ordering = ['id']
    inlines = [SubImages]
    
admin.site.register(Product, AdminProduct)
admin.site.register(Category)