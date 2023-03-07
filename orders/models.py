from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from shop.models import Product


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id}'

    @property
    def paid(self):
        return self.payment.completed

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def get_amount_paid(self):
        return self.payment.get_amount_paid()

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_balance(self):
        return self.get_total_cost() - self.get_amount_paid()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.product)

    def get_cost(self):
        return self.price * self.quantity
