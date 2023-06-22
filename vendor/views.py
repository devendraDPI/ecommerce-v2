from django.shortcuts import get_object_or_404, redirect, render
from account.models import UserProfile
from product.forms import CategoryForm, ProductForm
from product.models import Category, Product
from vendor.forms import VendorForm
from account.forms import UserProfileForm
from vendor.models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from account.utils import is_vendor
from vendor.utils import get_vendor
from django.template.defaultfilters import slugify


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


@login_required(login_url='signin')
@user_passes_test(is_vendor)
def category(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('name')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/category.html', context)


@login_required(login_url='signin')
@user_passes_test(is_vendor)
def products_by_category(request, pk=None):
    vendor = get_vendor(request)
    category_ = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(vendor=vendor, category=category_)
    context = {
        'category': category_,
        'products': products,
    }
    return render(request, 'vendor/products-by-category.html', context)


@login_required(login_url='signin')
@user_passes_test(is_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            new_category = form.save(commit=False)
            new_category.vendor = get_vendor(request)
            new_category.save()
            new_category.slug = f'{slugify(name)}-{new_category.id}'
            new_category.save()
            messages.success(request, 'Category added')
            return redirect('category')
        messages.error(request, 'Something went wrong')
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add-category.html', context)


@login_required(login_url='signin')
@user_passes_test(is_vendor)
def edit_category(request, pk=None):
    category_ = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category_)
        if form.is_valid():
            name = form.cleaned_data['name']
            new_category = form.save(commit=False)
            new_category.vendor = get_vendor(request)
            new_category.slug = slugify(name)
            new_category.save()
            messages.success(request, 'Category updated')
            return redirect('category')
        messages.error(request, 'Something went wrong')
    else:
        form = CategoryForm(instance=category_)
    context = {
        'category': category_,
        'form': form,
    }
    return render(request, 'vendor/edit-category.html', context)


@login_required(login_url='signin')
@user_passes_test(is_vendor)
def delete_category(request, pk=None):
    category_ = get_object_or_404(Category, pk=pk)
    category_.delete()
    messages.success(request, 'Category deleted')
    return redirect('category')


@login_required(login_url='signin')
@user_passes_test(is_vendor)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            new_product = form.save(commit=False)
            new_product.vendor = get_vendor(request)
            new_product.save()
            new_product.slug = f'{slugify(name)}-{new_product.id}'
            new_product.save()
            messages.success(request, 'Product added')
            return redirect('products-by-category', new_product.category.id)
        messages.error(request, 'Something went wrong')
    else:
        form = ProductForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
    }
    return render(request, 'vendor/add-product.html', context)


@login_required(login_url='signin')
@user_passes_test(is_vendor)
def edit_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            name = form.cleaned_data['name']
            product = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug = slugify(name)
            product.save()
            messages.success(request, 'Product updated')
            return redirect('products-by-category', product.category.id)
        messages.error(request, 'Something went wrong')
    else:
        form = ProductForm(instance=product)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'vendor/edit-product.html', context)


@login_required(login_url='signin')
@user_passes_test(is_vendor)
def delete_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted')
    return redirect('products-by-category', product.category.id)
