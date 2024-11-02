from django.shortcuts import redirect, render
from accounts.models import User

# Create your views here.
def homepage(request):
    user = User.objects.get(uid = request.user.uid)

    if user.user_type == 'Vendor':
        return redirect('vendor:homepage')
    
    return render(request, 'customer/homepage.html')