from marketplace.models import Cart
from product.models import Product


def get_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            if cart_items := Cart.objects.filter(user=request.user):
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return {'cart_count': cart_count}


def get_cart_amount(request):
    subtotal = 0
    tax = 0
    total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            product = Product.objects.get(pk=item.product.id)
            subtotal += (product.price * item.quantity)
        total = subtotal + tax
    return {'subtotal': subtotal, 'tax': tax, 'total': total}
