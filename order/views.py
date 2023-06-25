from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from account.utils import send_notification_email
from marketplace.context_processors import get_cart_amount
from marketplace.models import Cart
from order.forms import OrderForm
from order.models import Order, OrderedProduct, Payment
import simplejson as json
from order.utils import generate_order_number
from django.contrib.auth.decorators import login_required
import razorpay
from the_shop.settings import RZP_KEY_ID, RZP_KEY_SECRET


client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))


@login_required(login_url='signin')
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
            # Razorpay
            DATA = {
                'amount': float(order.total) * 100,
                'currency': 'INR',
                'receipt': f'receipt#{order.order_number}',
                'notes': {
                    'key1': 'value3',
                    'key2': 'value2'
                }
            }
            rzp_order = client.order.create(data=DATA)
            rzp_order_id = rzp_order['id']
            context = {
                'order': order,
                'cart_items': cart_items,
                'rzp_order_id': rzp_order_id,
                'RZP_KEY_ID': RZP_KEY_ID,
                'rzp_amount': float(order.total) * 100,
            }
            return render(request, 'order/place-order.html', context)
        messages.error(request, 'Something went wrong')
    return render(request, 'order/place-order.html')


@login_required(login_url='signin')
def payment(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # Store the payment details in the payment model
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        order = Order.objects.get(user=request.user, order_number=order_number)
        payment_ = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount=order.total,
            status=status,
        )
        payment_.save()
        # Update the order model
        order.payment = payment_
        order.is_ordered = True
        order.save()
        # Move the cart items to the ordered product model
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_product = OrderedProduct()
            ordered_product.order = order
            ordered_product.payment = payment_
            ordered_product.user = request.user
            ordered_product.product = item.product
            ordered_product.quantity = item.quantity
            ordered_product.price = item.product.price
            ordered_product.amount = item.product.price * item.quantity
            ordered_product.save()
        # Send order received email to customer
        mail_subject = 'Thankyou for your order'
        mail_template = 'order/email/order-confirmation-email.html'
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,
        }
        send_notification_email(mail_subject, mail_template, context)
        # Send order received email to vendor
        mail_subject = 'Received new order'
        mail_template = 'order/email/new-order-received-email.html'
        to_eamils = list({v.product.vendor.user.email for v in cart_items})
        context = {
            'order': order,
            'to_email': to_eamils,
        }
        send_notification_email(mail_subject, mail_template, context)
        # Clear the cart items if payment is successful
        cart_items.delete()
        # Retuen order status
        response = {
            'order_number': order_number,
            'transaction_id': transaction_id,
        }
        return JsonResponse(response)
    return HttpResponse('Payment view')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transaction_id = request.GET.get('transaction_id')
    try:
        order = Order.objects.get(
            order_number=order_number,
            payment__transaction_id=transaction_id,
            is_ordered=True,
        )
        ordered_product = OrderedProduct.objects.filter(order=order)
        subtotal = sum(item.price * item.quantity for item in ordered_product)
        tax_data = json.loads(order.tax_data)
        context = {
            'order': order,
            'ordered_product': ordered_product,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }
        return render(request, 'order/order-complete.html', context)
    except:
        return redirect('home')
