from django.db import models
from account.models import User
from product.models import Product
from vendor.models import Vendor
import simplejson as json


PAYMENT_METHOD = (
    ('paypal', 'PayPal'),
    ('razorpay', 'RazorPay'),
)


ORDER_STATUS = (
    ('received', 'Received'),
    ('accepted', 'Accepted'),
    ('in_transit', 'In Transit'),
    ('out_for_delivery', 'Out For Delivery'),
    ('cancelled', 'Cancelled'),
    ('delivered', 'Delivered'),
)


request_object = ''


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=256)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=128)
    amount = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=256)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)
    email = models.EmailField(max_length=128)
    address = models.CharField(max_length=512)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    pin_code = models.CharField(max_length=8)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text = "{'type': {'percentage': 'amount'}}")
    all_data = models.JSONField(blank=True, null=True, help_text="{'vendor_id': {'subtotal': {'tax_type': {'tax_percentage': 'tax_amount'}}}}")
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=128)
    status = models.CharField(max_length=32, choices=ORDER_STATUS, default='received')
    is_ordered = models.BooleanField(default=False)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def order_placed_to(self):
        return ", ".join([str(i) for i in self.vendors.all()])

    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        subtotal = 0
        tax = 0
        tax_dict = {}
        if self.all_data:
            all_data = json.loads(self.all_data)
            data = all_data.get(str(vendor.id))
            for key, val in data.items():
                subtotal += float(key)
                tax_dict.update(val)
            for i in val:
                for j in val[i]:
                    tax += float(val[i][j])
        total = float(subtotal) + float(tax)
        return {
            'subtotal': subtotal,
            'tax_dict': tax_dict,
            'total': total,
        }

    def __str__(self):
        return self.order_number


class OrderedProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()

    def __str__(self):
        return self.product.name
