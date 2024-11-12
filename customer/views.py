from decimal import Decimal
import json
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from accounts.models import User
from products.models import *
from customer.models import Cart, CartItem
from vendor.models import Cupon

# Create your views here.
def homepage(request):
    user = User.objects.get(uid = request.user.uid)
    if user.user_type == 'Vendor':
        return redirect('vendor:homepage')
    
    category = Category.objects.all().order_by('name')
    products = Product.objects.filter(stock__gte = 1).order_by('?')[:12]
    return render(request, 'customer/homepage.html',{
        'categories' : category,
        'products' : products
    })

def products(request):
    categorys = Category.objects.all()
    products = Product.objects.filter(stock__gte=1).order_by('?')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        categories = request.GET.getlist('categorys')

        if categories:
            category_filter = Q()
            for category in categories:
                category_filter |= Q(category__name=category)
            
            product_data = products.filter(category_filter).order_by('?')

            return render(request, 'customer/ajax/products.html', {
                'categorys': categorys,
                'products': product_data
            })
        
    return render(request, 'customer/products.html', {
        'categorys': categorys,
        'products': products
    })

def product_details(request, slug):
    product = Product.objects.get(slug = slug)
    related_products = Product.objects.filter(
        Q(vendor = product.vendor) | Q(category = product.category)
    ).exclude(slug = product.slug).order_by('?')[:4]

    return render(request, 'customer/product_details.html',{
        'product' : product,
        'related_products' : related_products
    })


@login_required(login_url='http://127.0.0.1:8000/login/')
def add_to_cart(request, pid):
    try:
        product = Product.objects.get(uid = pid)

        cart, _ = Cart.objects.get_or_create(
            user = request.user,
            is_paid = False
        )

        cart_item = CartItem.objects.create(
            cart = cart,
            product = product,
            quantity = request.GET.get('quantity')
        )

        if request.GET.get('size'):
            cart_item.size_variant = SizeVariant.objects.get(name = request.GET.get('size'))

        if request.GET.get('color'):
            cart_item.color_variant = ColorVariant.objects.get(name = request.GET.get('color'))

        cart_item.save()
        
        messages.success(request, message="Product added to cart.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def view_cart(request):
    cart = Cart.objects.get(user = request.user, is_paid = False)
    return render(request, 'customer/cart.html', {
        'cart' : cart,
        'cart_items' : cart.cart_items.all()
    })


def remove_from_cart(request, slug, cid):
    cart = Cart.objects.get(uid = cid)
    product = Product.objects.get(slug = slug)
    CartItem.objects.get(cart = cart, product = product).delete()
    messages.success(request, message=f"{product.name} removed from cart.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cupon_verification(request):
    try:
        if request.method == 'POST':
            vendors = []
            code = request.POST.get('cupon_code')
            cart = Cart.objects.get(uid = request.POST.get('cart'))
            cupon = Cupon.objects.get(coupon_code = code)
            items = CartItem.objects.filter(cart = cart)
            
            for item in items:
                vendors = item.product.vendor.email
            
            if Decimal(request.POST.get('payable')) < cupon.minimum_amount:
                return JsonResponse({
                    'message' : f"You Need To Purchase More Than {cupon.minimum_amount} To Apply This Cupon.",
                    'message_type' : 'error'
                })
            
            elif cupon.vendor.email in vendors:
                return JsonResponse({
                    'message' : "Cupon is Applyed.",
                    'message_type' : 'success',
                    'discount' : cupon.discount_price,
                    'total_price' : cart.total_price() - cupon.discount_price
                })
            
            else:
                return JsonResponse({
                    'message' : 'Cupon Is Not Applicable For This Products.',
                    'message_type' : 'error'
                })
            
    except Cupon.DoesNotExist:
        return JsonResponse({
            'message' : f'{code} Cupon Is Not Found.',
            'message_type' : 'error'
        })
    
    return JsonResponse({'message': 'Coupon code received successfully!'},)