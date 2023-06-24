from django.db import models
from account.models import User
from product.models import Product


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
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=128)
    status = models.CharField(max_length=32, choices=ORDER_STATUS, default='received')
    is_ordered = models.BooleanField(default=False)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

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
