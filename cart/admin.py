from django.contrib import admin
from . models import Cart


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'product', 'quantity', 'price']
    ordering = ['id']
admin.site.register(Cart, AdminProduct)