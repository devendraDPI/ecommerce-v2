from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from account.models import UserProfile
from marketplace.context_processors import get_cart_count, get_cart_amount
from marketplace.models import Cart
from order.forms import OrderForm
from product.models import Category, Product
from vendor.models import OpeningHour, Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from datetime import date


def marketplace(request):
    vendors = Vendor.objects.filter(user__is_active=True, is_approved=True).order_by('modified_at')
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/marketplace.html', context)


def vendor_details(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'product',
            queryset = Product.objects.filter(is_available=True).order_by('name')
        )
    ).order_by('name')
    operating_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')
    today_date = date.today()
    today = today_date.isoweekday()
    today_operating_hours = OpeningHour.objects.filter(vendor=vendor, day=today)
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user)
    else:
        cart_item = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_item': cart_item,
        'operating_hours': operating_hours,
        'today_operating_hours': today_operating_hours,
    }
    return render(request, 'marketplace/vendor-details.html', context)


def increment_cart_item(request, id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if product exists
            try:
                product = Product.objects.get(id=id)
                # Check if user has already added product to cart
                try:
                    check_cart = Cart.objects.get(user=request.user, product=product)
                    # Increase the cart quantity
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Cart quantity increased',
                        'cart_count': get_cart_count(request),
                        'quantity': check_cart.quantity,
                        'cart_amount': get_cart_amount(request)
                    })
                except:
                    check_cart = Cart.objects.create(user=request.user, product=product, quantity=1)
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Product added to the cart',
                        'cart_count': get_cart_count(request),
                        'quantity': check_cart.quantity,
                        'cart_amount': get_cart_amount(request)
                    })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'This product does not exists'
                })
        else:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid request'
            })
    else:
        return JsonResponse({
            'status': 'signin_required',
            'message': 'Signin to continue'
        })


def decrement_cart_item(request, id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if product exists
            try:
                product = Product.objects.get(id=id)
                # Check if user has already added product to cart
                try:
                    check_cart = Cart.objects.get(user=request.user, product=product)
                    if check_cart.quantity > 1:
                        # Decrease the cart quantity
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Cart quantity decreased',
                        'cart_count': get_cart_count(request),
                        'quantity': check_cart.quantity,
                        'cart_amount': get_cart_amount(request)
                    })
                except:
                    return JsonResponse({
                        'status': 'Failed',
                        'message': 'This product is not in your cart'
                    })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'This product does not exists'
                })
        else:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid request'
            })
    else:
        return JsonResponse({
            'status': 'signin_required',
            'message': 'Signin to continue'
        })


@login_required(login_url = 'signin')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart_item(request, id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if product in cart exists
            try:
                cart_item = Cart.objects.get(user=request.user, id=id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Cart item deleted',
                        'cart_count': get_cart_count(request),
                        'cart_amount': get_cart_amount(request)
                    })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'Product does not exists in the cart'
                })
        else:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid request'
            })


def search(request):
    # if 'address' not in request.GET:
    #     return redirect('marketplace')
    query = request.GET.get('q')
    address = request.GET.get('address')
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lng')
    radius = request.GET.get('radius')
    fetch_vendors_by_product = Product.objects.filter(
        name__icontains=query,
        is_available=True,
    ).values_list('vendor', flat=True)
    fetch_vendors_by_category = Category.objects.filter(
        name__icontains=query,
    ).values_list('vendor', flat=True)
    vendors = Vendor.objects.filter(
        Q(id__in=fetch_vendors_by_product) |
        Q(id__in=fetch_vendors_by_category) |
        Q(name__icontains=query, is_approved=True, user__is_active=True)
    )
    if latitude and longitude and radius:
        point = GEOSGeometry(f'POINT({longitude} {latitude})', srid=4326)
        vendors = Vendor.objects.filter(
            Q(id__in=fetch_vendors_by_product) |
            Q(id__in=fetch_vendors_by_category) |
            Q(name__icontains=query, is_approved=True, user__is_active=True),
            user_profile__location__distance_lte=(point, D(km=radius))
        ).annotate(distance=Distance("user_profile__location", point)).order_by("distance")
        for distance_ in vendors:
            distance_.kms = round(distance_.distance.km, 2)
    context = {
        'vendors': vendors,
        'vendor_count': vendors.count(),
        'source_location': address,
    }
    return render(request, 'marketplace/marketplace.html', context)


@login_required(login_url = 'signin')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    cart_items_count = cart_items.count()
    if cart_items_count < 1:
        return redirect('marketplace')
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone,
        'email': request.user.email,
        'address': user_profile.address,
        'city': user_profile.city,
        'state': user_profile.state,
        'country': user_profile.country,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/checkout.html', context)
