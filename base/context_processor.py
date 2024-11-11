from customer.models import Cart, CartItem

# cart count
def cart_item_count(request):
    count = 0
    if request.user.is_authenticated and request.user.user_type == 'Customer':
        try:
            cart = Cart.objects.get(user = request.user, is_paid = False)
            count = CartItem.objects.filter(cart = cart).count()
        except Cart.DoesNotExist as e:
            print(e)
    return {
        'cart_count' : count
    }