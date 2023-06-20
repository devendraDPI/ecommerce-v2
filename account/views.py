from django.shortcuts import redirect, render
from account.forms import UserSignupForm
from account.models import User, UserProfile
from django.contrib import auth, messages
from account.utils import detect_user, send_email, is_customer, is_vendor
from vendor.forms import VendorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify


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
            mail_subject = 'Activate your account'
            email_template = 'account/email/account-verification.html'
            send_email(request, mail_subject, email_template, user)
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
        vendor_form = VendorForm(request.POST, request.FILES)
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
            name = vendor_form.cleaned_data['name']
            vendor.slug = f'{slugify(name)}-{user.id}'
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            mail_subject = 'Activate your account'
            email_template = 'account/email/account-verification.html'
            send_email(request, mail_subject, email_template, user)
            messages.success(request, 'Your account has been created successfully')
            return redirect('vendor-signup')
    else:
        form = UserSignupForm()
        vendor_form = VendorForm()
    context = {
        'form': form,
        'vendor_form': vendor_form,
    }
    return render(request, 'account/vendor-signup.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated')
        return redirect('dashboard')
    messages.error(request, 'Invalid activation link')
    return redirect('dashboard')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            mail_subject = 'Reset your account password'
            email_template = 'account/email/reset-password.html'
            send_email(request, mail_subject, email_template, user)
            messages.success(request, 'Password reset link has been sent')
            return redirect('signin')
        messages.error(request, 'Account does not exist')
        return redirect('forgot-password')
    return render(request, 'account/forgot-password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Reset your password')
        return redirect('reset-password')
    messages.error(request, 'Link expired')
    return redirect('dashboard')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.save()
            messages.success(request, 'Passwords reset successful')
            return redirect('signin')
        messages.error(request, 'Passwords do not match')
        return redirect('reset-password')
    return render(request, 'account/reset-password.html')


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
