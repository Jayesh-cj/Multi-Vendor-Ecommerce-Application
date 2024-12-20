from decimal import Decimal
import uuid
from django.db import models
from base.models import BaseModel
from accounts.models import User
from products.models import Product, ColorVariant, SizeVariant

# Create your models here.
class Cupon(BaseModel):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_vendor')
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.DecimalField(decimal_places=2, max_digits=7, default=100.00, verbose_name="Discount Price")
    minimum_amount = models.DecimalField(decimal_places=2, max_digits=8, default=500.00, verbose_name="Minimum Purchase Amount")

    def __str__(self) -> str:
        return f"{self.vendor} - cupon code = {self.coupon_code}"
    
    class Meta:
        ordering = ['created_at']


class Payment(BaseModel):
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default='Pending')
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Payment for Order of {self.user} - {self.status}"


class Order(BaseModel):
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='order_payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=100, choices=ORDER_STATUS, default='Pending')
    shipping_address = models.TextField(null=True, blank=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_vendor')
    cupon = models.ForeignKey(Cupon, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name="order_cupon")
    payable = models.DecimalField(decimal_places=2, max_digits=10)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order by {self.user}"
    
    def save(self, *args, **kwargs) -> None:
        if self.cupon:
            discount = self.cupon.discount_price
            self.payable = (self.total_amount - discount)
        else:
            self.payable = self.total_amount

        super(Order, self).save(*args, **kwargs)
    
    def get_order_total_price(self):
        order_total = Decimal(0.0)
        discount = self.cupon.discount_price if self.cupon else 00
        vendors = []

        for item in self.items.all():
            order_total += item.total_price
            vendors.append(item.produt_vendors)

        final_price = order_total
        
        if self.cupon.vendor in vendors:
            final_price = order_total - self.cupon.discount_price

        return {
            'order_total' : order_total,
            'discount' : discount,
            'final_price' : final_price
        }
    
    class Meta:
            ordering = ['created_at']


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    product_color = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='item_color')
    product_size = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='item_size')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=8)

    @property
    def total_price(self):
        return self.price * self.quantity
    
    @property
    def produt_vendors(self):
        return self.product.vendor