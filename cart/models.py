from django.db import models
from django.contrib import admin
from store.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    phone_number = models.CharField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.name