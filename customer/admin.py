from django.contrib import admin
from customer.models import Cart, CartItem

# Register your models here.
admin.site.register(Cart)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'color_variant', 'size_variant', 'quantity' ]