from django.contrib import admin
from products.models import *

# Register your models here.
admin.site.register(Category)

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProductImagesAdmin(admin.StackedInline):
    model = ProductImages

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name','category', 'vendor', 'price']
    inlines = [ProductImagesAdmin]

admin.site.register(Product, ProductsAdmin)