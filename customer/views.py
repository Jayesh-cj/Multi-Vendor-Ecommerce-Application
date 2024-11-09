from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from accounts.models import User
from base.context_processor import cart_item_count
from products.models import *
from customer.models import Cart, CartItem

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
