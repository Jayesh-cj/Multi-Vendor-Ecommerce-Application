from django.shortcuts import render
from accounts.models import User

# Create your views here.
def homepage(request):
    try:
        vendor = User.objects.get(uid = request.user.uid)
    except Exception as e:
        print(e)
    return render(request,'vendor/homepage.html',{
        'vendor' : vendor
    })


def view_products(request):
    return render(request, 'vendor/products.html')