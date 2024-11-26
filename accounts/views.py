from django.http import HttpResponseRedirect, JsonResponse
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
        
    return render(request,'authentication/signup.html')


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
            
            else:
                user_auth_obj = authenticate(request, email = email, password = password)
                if user_auth_obj:
                    login(request, user_auth_obj)

                    if user_auth_obj.user_type == 'Customer':
                        return redirect('customer:homepage')
                    elif user_auth_obj.user_type == 'Vendor':
                        return redirect('vendor:homepage')
                
                else:
                    messages.warning(request, message='Incorrect password or email')
                    return HttpResponseRedirect(redirect_to=request.path_info)

    except User.DoesNotExist:
        messages.warning(request, message='Account not found')
        return HttpResponseRedirect(redirect_to=request.path_info)

    return render(request, 'authentication/login.html')


def logout_user(request):
    logout(request)
    return redirect('accounts:login')


def profile(request):
    user = request.user
    if user.is_authenticated:
        if user.user_type == 'Customer':
            return render(request, 'customer/profile.html', {
                'user' : user
            })
    else:
        return redirect('accounts:login')
    

def update_profile(request, uid):
    user = User.objects.get(uid = uid)
    profile = request.FILES.get('profile')

    if profile:
        user.profile = profile
    
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.username = request.POST.get('username')
    user.email = request.POST.get('email')
    user.phone = request.POST.get('phone')
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_address(request, user):
    user = User.objects.get(uid = user)
    Contacts.objects.create(
        user = user,
        address = request.POST.get('txt_address')
    )
    messages.success(request, "New Address Added successfully.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_address(request):
    address = Contacts.objects.get(
        user = request.user,
        id = request.POST.get('address_id')
    )
    address.address = request.POST.get('txt_address')
    address.save()
    messages.success(request, "Address Updated Successfully. ")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_address(request, address):
    address = Contacts.objects.get(id = address)
    address.delete()
    messages.success(request, "Address Deleted Successfully. ")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
