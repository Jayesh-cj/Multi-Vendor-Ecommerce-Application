from django.contrib import admin
from vendor.models import *

# Register your models here.
@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'vendor', 'is_expired', 'discount_price', 'minimum_amount']

class OrderItemAdmin(admin.StackedInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'vendor', 'status', 'payment']
    inlines = [OrderItemAdmin]

@admin.register(OrderItem)
class OrderItemDisplay(admin.ModelAdmin):
    list_display = ['order', 'product', 'product_color', 'product_size', 'quantity', 'price']

admin.site.register(Payment)