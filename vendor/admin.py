from django.contrib import admin
from vendor.models import Cupon

# Register your models here.
@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'vendor', 'is_expired', 'discount_price', 'minimum_amount']