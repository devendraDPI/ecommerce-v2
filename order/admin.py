from django.contrib import admin
from order.models import Order, OrderedProduct, Payment

class OrderProductInline(admin.TabularInline):
    model = OrderedProduct
    readonly_fields = ('product', 'quantity', 'price', 'amount', 'payment', 'user')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'last_name', 'phone', 'email',
                    'pin_code', 'total', 'status', 'order_placed_to', 'payment_method',
                    'is_ordered', 'created_at')
    inlines = (OrderProductInline,)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedProduct)
admin.site.register(Payment)
