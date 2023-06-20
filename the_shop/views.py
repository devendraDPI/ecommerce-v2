from django.shortcuts import render
from vendor.models import Vendor


def home(request):
    featured_vendors = Vendor.objects.filter(user__is_active=True, is_approved=True, is_featured=True).order_by('modified_at')
    vendors = Vendor.objects.filter(user__is_active=True, is_approved=True, is_featured=False).order_by('modified_at')[:9]
    context = {
        'featured_vendors': featured_vendors,
        'vendors': vendors,
    }
    return render(request, 'home.html', context)
