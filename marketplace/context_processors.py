from marketplace.models import Cart, Tax
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
    tax_dict = {}
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            product = Product.objects.get(pk=item.product.id)
            subtotal += (product.price * item.quantity)
        get_tax = Tax.objects.filter(is_active=True)
        for i in get_tax:
            tax_type = i.tax_type
            percentage = i.percentage
            tax_amount = round((percentage * subtotal) / 100, 2)
            tax_dict[tax_type] = {str(percentage): tax_amount}
        tax = sum(x for key in tax_dict.values() for x in key.values())
        total = subtotal + tax
    return {'subtotal': subtotal, 'tax_dict': tax_dict, 'tax': tax, 'total': total}
