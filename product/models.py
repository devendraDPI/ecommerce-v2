from django.db import models
from vendor.models import Vendor


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=256, unique=True)
    description = models.TextField(max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def clean(self):
        self.name = self.name.capitalize()

    def __str__(self):
        return self.name


class Product(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=512, unique=True)
    description = models.TextField(max_length=16384, blank=True)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
