from django.shortcuts import redirect, render
from accounts.models import User
from products.models import Category, Product
from django.db.models import Q

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