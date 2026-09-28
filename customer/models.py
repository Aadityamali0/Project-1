from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=15)
    
    def register(self):
        self.save()
    
    def __str__(self):
        return self.name
    
# class LoginImageGroup(models.Model):
#     name = models.CharField(default="Login and Register Image")
    
#     def __str__(self):
#         return self.name

# class IndividualImage(models.Model):
#     group = models.ForeignKey(LoginImageGroup, on_delete=models.CASCADE, related_name="images")
#     image = models.ImageField(upload_to="customer/images")