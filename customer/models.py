from django.db import models
from accounts.models import User
from products.models import Product, ColorVariant, SizeVariant
from base.models import BaseModel
from vendor.models import Cupon

# Create your models here.
class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contacts')
    address = models.TextField()

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.first_name}"
    
    def get_cart_items_count(self):
        return CartItem.objects.filter(cart__is_paid = False, cart__user = self.user).count()


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart')
    cupon = models.ForeignKey(Cupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_cupon')
    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}'s Cart"
    
    def total_price(self):
        total_price = []
        for item in self.cart_items.all():
            price = item.product.price
            total_price.append(price * item.quantity)
        return sum(total_price)
       

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity  = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.product.name
    
    class Meta:
        ordering = ['created_at']