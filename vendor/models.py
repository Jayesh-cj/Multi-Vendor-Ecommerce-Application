from django.db import models
from base.models import BaseModel
from accounts.models import User
from products.models import Product

# Create your models here.
class Cupon(BaseModel):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_vendor')
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.DecimalField(decimal_places=2, max_digits=7, default=100.00)
    minimum_amount = models.DecimalField(decimal_places=2, max_digits=8, default=500.00)

    def __str__(self) -> str:
        return f"{self.vendor} - cupon code = {self.coupon_code}"
    

class Order(BaseModel):
    ORDER_STATUS = (
        ('Pending','Pending'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='oredered_user')
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=100, choices=ORDER_STATUS, default='Pending')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} order"
    

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='ordered_product')
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=8)