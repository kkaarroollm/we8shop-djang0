from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import SizeOption, ProductImage, Products, ProductStock
from users.models import User


class Order(models.Model):
    STATUS_CHOICES = (
        ('RECEIVED', 'Received'),
        ('SHIPPED', 'Shipped'),
        ('CANCELLED', 'Cancelled'),
    )

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RECEIVED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(SizeOption, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'product', 'size')

    def __str__(self):
        return f"{self.product.name} ({self.size})"

    '''while adding in admin function clean validate whether the product in this size is available 
    and quantity of the product in that size'''
    def clean(self):
        stock = ProductStock.objects.filter(product=self.product, size=self.size, stock__gt=0)
        if not stock:
            raise ValidationError(f"{self.product.name} is not available in size {self.size}")
        else:
            stock = stock.first()
            if self.quantity > stock.stock:
                raise ValidationError(f"stock of {self.product.name} ({self.size}) has only {stock.stock} available")
            self.price = stock.product.price

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ShippingAddresses(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.address


'''this signal is executed each time the order is placed, it takes the quantity of the order product 
and decrease the stock in db'''


@receiver(post_save, sender=OrderItem)
def update_product_stock(instance, created, **kwargs):
    if created:
        product_stock = ProductStock.objects.get(product=instance.product, size=instance.size)
        product_stock.stock -= instance.quantity
        product_stock.save()
