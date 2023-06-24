from django import forms
from account.models import User, UserProfile
from account.validators import allow_only_images_validator


class UserSignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'last name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'

    def clean(self):
        cleaned_data = super(UserSignupForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('Passwords do not match.')


class UserProfileForm(forms.ModelForm):
    profile_image = forms.FileField(widget=forms.FileInput(attrs={'placeholder': 'profile image', 'style': 'padding-top: 0rem; line-height: 3.2;'}), validators=[allow_only_images_validator])
    cover_image = forms.FileField(widget=forms.FileInput(attrs={'placeholder': 'cover image', 'style': 'padding-top: 0rem; line-height: 3.2;'}), validators=[allow_only_images_validator])
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'city'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'state'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'country'}))
    pin_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'pin code'}))
    latitude = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'latitude', 'readonly': 'readonly'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'longitude', 'readonly': 'readonly'}))

    class Meta:
        model = UserProfile
        fields = ['profile_image', 'cover_image', 'address', 'city', 'state', 'country', 'pin_code', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'


class UserInfoForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'last name'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'phone'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'
