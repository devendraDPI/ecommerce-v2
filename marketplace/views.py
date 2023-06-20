from django.shortcuts import get_object_or_404, render
from product.models import Category, Product
from vendor.models import Vendor
from django.db.models import Prefetch


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
    context = {
        'vendor': vendor,
        'categories': categories,
    }
    return render(request, 'marketplace/vendor-details.html', context)
