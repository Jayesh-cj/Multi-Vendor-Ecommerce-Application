from django.shortcuts import render
from accounts.models import *

# Create your views here.
def home_page(request):
    user = User.objects.get(uid = request.user.uid)
    return render(request, 'homepage.html',{
        'user' : user
    })