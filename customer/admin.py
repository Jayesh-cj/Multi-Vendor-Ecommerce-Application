from django.contrib import admin
from customer.models import Cart, CartItem

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)