from django.shortcuts import redirect, render
from accounts.models import User
from products.models import *

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