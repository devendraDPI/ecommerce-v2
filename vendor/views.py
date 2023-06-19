from django.shortcuts import get_object_or_404, redirect, render
from account.models import UserProfile
from vendor.forms import VendorForm
from account.forms import UserProfileForm
from vendor.models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from account.utils import is_vendor


@login_required(login_url='signin')
@user_passes_test(is_vendor)
def vendor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Profile updated')
            return redirect('vendor-profile')
        messages.error(request, 'Something went wrong')
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile': profile,
        'vendor': vendor,
        'profile_form': profile_form,
        'vendor_form': vendor_form,
    }
    return render(request, 'vendor/vendor-profile.html', context)
