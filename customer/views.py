from django.shortcuts import get_object_or_404, redirect, render
from account.forms import UserProfileForm, UserInfoForm
from account.utils import is_customer
from django.contrib.auth.decorators import login_required, user_passes_test
from account.models import UserProfile
from django.contrib import messages
from order.models import Order, OrderedProduct
import simplejson as json


@login_required(login_url='signin')
@user_passes_test(is_customer)
def customer_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('customer-profile')
        messages.error(request, 'Something went wrong')
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)
    context = {
        'profile': profile,
        'profile_form': profile_form,
        'user_form': user_form,
    }
    return render(request, 'customer/customer-profile.html', context)


@login_required(login_url='signin')
@user_passes_test(is_customer)
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'customer/my-orders.html', context)


@login_required(login_url='signin')
@user_passes_test(is_customer)
def order_details(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_product = OrderedProduct.objects.filter(order=order)
        subtotal = sum((item.price * item.quantity) for item in ordered_product)
        tax_data = json.loads(order.tax_data)
        context = {
            'order': order,
            'ordered_product': ordered_product,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }
        return render(request, 'customer/order-details.html', context)
    except:
        return redirect('customer-dashboard')
