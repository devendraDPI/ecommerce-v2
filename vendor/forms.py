from django import forms
from vendor.models import Vendor
from account.validators import allow_only_images_validator


class VendorForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'vendor name'}))
    license = forms.FileField(widget=forms.FileInput(attrs={'placeholder': 'license', 'style': 'padding-top: 0rem; line-height: 3.2;'}), validators=[allow_only_images_validator])

    class Meta:
        model = Vendor
        fields = ['name', 'license']

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'
