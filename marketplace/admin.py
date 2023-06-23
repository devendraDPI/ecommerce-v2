from django.contrib import admin
from marketplace.models import Cart, Tax


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'updated_at', 'created_at')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'percentage', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(Tax, TaxAdmin)
