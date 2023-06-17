from django import forms
from vendor.models import Vendor


class VendorSignupForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control my-2', 'placeholder': 'vendor name'}))
    license = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'class': 'form-control my-2', 'style': 'padding-top: 0rem; line-height: 3.2;', 'placeholder': 'license'}))

    class Meta:
        model = Vendor
        fields = ['name', 'license']
