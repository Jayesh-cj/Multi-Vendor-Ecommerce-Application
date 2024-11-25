import razorpay

from collections import defaultdict

from decimal import Decimal
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from ecomm import settings
from ecomm.settings import LOGIN_URL
from products.models import *
from customer.models import Cart, CartItem, Contacts
from vendor.models import *

# Create your views here.
def homepage(request):
    user = request.user
    if user.is_authenticated:
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

    return render(request, 'customer/products.html', {
        'categorys': categorys,
        'products': products
    })


def fillter_products(request):
    all_categories = Category.objects.all()
    products = Product.objects.filter(stock__gte=1)

    context = {
        'categorys': all_categories,
        'products' : products
    }

    search = request.GET.get('search')
    categories = request.GET.getlist('categorys')

    if categories:
        category_filter = Q()
        for category in categories:
            category_filter |= Q(category__name=category)
        
        product_data = products.filter(category_filter).order_by('?')

        if search:
            product_data = product_data.filter(name__icontains = search)
            
        context['products'] = product_data
    
    if search:
        product_data = products.filter(name__icontains = search)
        context['products'] = product_data

    return render(request, 'customer/ajax/products.html', context)


def product_details(request, slug):
    product = Product.objects.get(slug = slug)
    related_products = Product.objects.filter(
        Q(vendor = product.vendor) | Q(category = product.category)
    ).exclude(slug = product.slug).order_by('?')[:4]

    return render(request, 'customer/product_details.html',{
        'product' : product,
        'related_products' : related_products
    })


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
    total = cart.total_price()
    
    if cart.cupon:
        discount = cart.cupon.discount_price
    else:
        discount = 00.0

    return render(request, 'customer/cart.html', {
        'cart' : cart,
        'cart_items' : cart.cart_items.all(),
        'discount' : discount,
        'total_price' : total,
        'payable' : (total - Decimal(discount))
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
                vendors.append(item.product.vendor.email)
            
            if Decimal(request.POST.get('payable')) < cupon.minimum_amount:
                return JsonResponse({
                    'message' : f"You Need To Purchase More Than {cupon.minimum_amount} To Apply This Cupon.",
                    'message_type' : 'error'
                })
            
            elif cart.cupon == cupon:
                return JsonResponse({
                    'message' : "Cupon Is Already Applyed.",
                    'message_type' : 'error'
                })
            
            elif cupon.vendor.email in vendors:
                cart.cupon = cupon
                cart.save()
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


def add_address(request):
    contact = Contacts.objects.create(
        user = request.user,
        address = request.POST.get('address')
    )
    contact.save()
    messages.success(request, message='Address Added.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url=LOGIN_URL)
def checkout(request):
    cart = Cart.objects.get(user = request.user, is_paid = False)
    address = Contacts.objects.filter(user = request.user)

    discount = cart.cupon.discount_price if cart.cupon else 00.00

  
    return render(request, 'customer/checkout.html', {
        'products' : cart,
        'total' : cart.total_price(),
        'discount' : discount,
        'payable' : (cart.total_price() - int(discount)),
        'address' : address
    })
    

# RazorePay Payment Order Creation
@csrf_exempt
def create_razorepay_order(request):
    try:
        amount = Decimal(request.POST.get('amount'))
        currency = 'INR'
        payable = int((amount * 100))
        api_key = settings.RAZORPAY_KEY_ID

        # razorepay client initialization
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # create razorpay Order
        order_data = {
            'amount': payable,  # Amount in paise
            'currency': currency,
            'payment_capture': '1',  # Auto-capture payment after authorization
        }

        order = client.order.create(data=order_data)

        payment_details = Payment.objects.create(
            user = request.user,
            amount = amount
        )

        cart_uid = request.POST.get('cart')
        address = Contacts.objects.get(id = request.POST.get('address_id')).address

        cart = Cart.objects.get(uid = cart_uid)
        items = CartItem.objects.filter(cart=cart)
        vendor_items = defaultdict(list)
        
        for item in items:
            vendor_items[item.product.vendor].append(item)

        for vendor, vendor_items_list in vendor_items.items():
            total_amount = sum(item.quantity * item.product.price for item in vendor_items_list)

            order_details = Order.objects.create(
                payment = payment_details,
                user = request.user,
                total_amount = total_amount,
                shipping_address = address,
                vendor = vendor,
                cupon = cart.cupon,
                payable = payable
            )

            for item in vendor_items_list:
                OrderItem.objects.create(
                    order = order_details,
                    product = item.product,
                    product_color = item.color_variant,
                    product_size = item.size_variant,
                    quantity = item.quantity,
                    price = (item.quantity * item.product.price)
                )

        return JsonResponse({
            'order_id' : order['id'],
            'payable' : payable,
            'api_key' : api_key
        })
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Something went wrong'}, status=500)
    

# Razorpay payment validation
def payment_validation(request):
    data = request.POST
    
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    cart = Cart.objects.get(uid = data['cart_id'])
    payment = cart.order_payment

    try:
        verified = client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        })

        if verified:
            payment.status = 'Completed'
            payment.save()

            cart.is_paid = True
            cart.save()
        else:
            payment.status = 'Failed'
            payment.save()
        
        return JsonResponse({
            'message' : 'Payment Sucessfull'
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            'error' : str(e)
        })
