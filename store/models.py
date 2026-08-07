from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null = True, blank = True)
    description = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="store/images", default="")
    
    def __str__(self):
        return self.product_name