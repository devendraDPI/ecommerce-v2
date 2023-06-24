from django.shortcuts import redirect, render
from django.contrib import messages
from marketplace.context_processors import get_cart_amount
from marketplace.models import Cart
from order.forms import OrderForm
from order.models import Order
import simplejson as json
from order.utils import generate_order_number


def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    cart_items_count = cart_items.count()
    if cart_items_count < 1:
        return redirect('marketplace')
    subtotal = get_cart_amount(request)['subtotal']
    tax_data = get_cart_amount(request)['tax_dict']
    tax = get_cart_amount(request)['tax']
    total = get_cart_amount(request)['total']
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.city = form.cleaned_data['city']
            order.state = form.cleaned_data['state']
            order.country = form.cleaned_data['country']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = tax
            order.payment_method = request.POST['payment_method']
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()
            return redirect('place-order')
        messages.error(request, 'Something went wrong')
    return render(request, 'order/place-order.html')
