from django import forms
from account.models import User


class UserSignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control my-2', 'placeholder': 'username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control my-2', 'placeholder': 'first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control my-2', 'placeholder': 'last name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control my-2', 'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control my-2', 'placeholder': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control my-2', 'placeholder': 'confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserSignupForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('Passwords do not match.')
