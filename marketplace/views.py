from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from marketplace.context_processors import get_cart_count, get_cart_amount
from marketplace.models import Cart
from product.models import Category, Product
from vendor.models import Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required


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
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user)
    else:
        cart_item = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_item': cart_item,
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
