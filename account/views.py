from django.shortcuts import redirect, render
from account.forms import UserSignupForm
from account.models import User, UserProfile
from django.contrib import auth, messages
from account.utils import detect_user
from vendor.forms import VendorSignupForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


def is_customer(user):
    """Returns True if the user us is customer"""
    if user.role == 'customer':
        return True
    raise PermissionDenied


def is_vendor(user):
    """Returns True if the user us is vendor"""
    if user.role == 'vendor':
        return True
    raise PermissionDenied


def user_signup(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already signed up')
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user.role = 'customer'
            user.save()
            messages.success(request, 'Your account has been created successfully')
            return redirect('user-signup')
    else:
        form = UserSignupForm()
    context = {
        'form': form,
    }
    return render(request, 'account/user-signup.html', context)


def vendor_signup(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already signed up')
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        vendor_form = VendorSignupForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user.role = 'vendor'
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been created successfully')
            return redirect('vendor-signup')
    else:
        form = UserSignupForm()
        vendor_form = VendorSignupForm()
    context = {
        'form': form,
        'vendor_form': vendor_form,
    }
    return render(request, 'account/vendor-signup.html', context)


def signin(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already signed in')
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have been signed in')
            return redirect('dashboard')
        messages.warning(request, 'Invalid sigin credentials')
        return redirect('signin')
    return render(request, 'account/signin.html')


def signout(request):
    auth.logout(request)
    messages.success(request, 'You have been signed out')
    return redirect('signin')


@login_required(login_url='signin')
def dashboard(request):
    user = request.user
    return redirect(detect_user(user))


@login_required(login_url='signin')
@user_passes_test(is_customer)
def customer_dashboard(request):
    return render(request, 'account/customer-dashboard.html')


@login_required(login_url='signin')
@user_passes_test(is_vendor)
def vendor_dashboard(request):
    return render(request, 'account/vendor-dashboard.html')
