from django import forms
from product.models import Category, Product
from account.validators import allow_only_images_validator


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'category name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'description'}))

    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'


class ProductForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'placeholder': 'product image', 'style': 'padding-top: 0rem; line-height: 3.2;'}), validators=[allow_only_images_validator])
    category = forms.Select(attrs={'placeholder': 'category'})
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'product name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'description'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'price', 'step':0.01}))

    class Meta:
        model = Product
        fields = ['image', 'category', 'name', 'description', 'price', 'is_available']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control my-2'
        self.fields['category'].widget.attrs['class'] = 'form-control my-2'
        self.fields['name'].widget.attrs['class'] = 'form-control my-2'
        self.fields['description'].widget.attrs['class'] = 'form-control my-2'
        self.fields['price'].widget.attrs['class'] = 'form-control my-2'
        self.fields['is_available'].widget.attrs['class'] = 'form-check-input'
