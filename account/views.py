from django.shortcuts import redirect, render
from account.forms import UserSignupForm
from account.models import User
from django.contrib import messages


def user_signup(request):
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
