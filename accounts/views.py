from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from accounts.models import *
from customer.models import Contacts

# Create your views here.
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(email = email).exists():
            messages.warning(request, message='This email is already exists.')
            return HttpResponseRedirect(redirect_to=request.path_info)
        
        elif password != confirm_password:
            messages.warning(request, message='Password Missmatch.')
            return HttpResponseRedirect(redirect_to=request.path_info)
        
        elif password == confirm_password:
            user = User.objects.create(
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                username = request.POST.get('username'),
                email = request.POST.get('email'),
                profile = request.FILES.get('profile'),
                user_type = request.POST.get('user_type'),
                phone = request.POST.get('phone')
            )

            if user.user_type == 'Customer':
                customer = Contacts.objects.create(
                    user = user,
                    address = request.POST.get('address')
                )
                customer.save()

            user.set_password(password)
            user.save()

            messages.success(request=request, message='An verification email has sent to your mail id check it out')
            return HttpResponseRedirect(redirect_to=request.path_info)
        
    return render(request,'signup.html')


def account_activation(request, token, email):
    try:
        user = User.objects.get(email_token = token)
        if user.email_token == token:
            user.is_verified = True
            user.save()
            messages.success(request, message='Your account activated successfully please login.')
            return redirect('accounts:login')
        else:
            message = messages.warning(request, message='Invalid user token.')
            return redirect('accounts:login')

    except Exception as e:
        print(e)


def account_login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = User.objects.get(email = email)

            if not user.is_verified:
                messages.warning(request, message='Your account is not verified! Pleasse check your email for verification')
                return HttpResponseRedirect(redirect_to=request.path_info)
            
            elif user.is_verified:
                user_auth_obj = authenticate(request, email = email, password = password)

                if user_auth_obj:
                    login(request, user_auth_obj)
                    return redirect('products:home')
                else:
                    messages.warning(request, message='Incorrect password')
                    return HttpResponseRedirect(redirect_to=request.path_info)

    except User.DoesNotExist:
        messages.warning(request, message='Account not found')
        return HttpResponseRedirect(redirect_to=request.path_info)

    return render(request, 'login.html')