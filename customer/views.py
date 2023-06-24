from django.shortcuts import get_object_or_404, redirect, render
from account.forms import UserProfileForm, UserInfoForm
from account.utils import is_customer
from django.contrib.auth.decorators import login_required, user_passes_test
from account.models import UserProfile
from django.contrib import messages


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
