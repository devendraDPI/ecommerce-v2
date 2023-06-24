from django import forms
from order.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'last name'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'phone'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'city'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'state'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'country'}))
    pin_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'pin code'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'city', 'state', 'country', 'pin_code']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'
