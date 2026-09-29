from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def total_quantity(self):
        # uses prefetched items when available
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} - {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(default=0)

    @property
    def line_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
