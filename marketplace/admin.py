from django.contrib import admin
from marketplace.models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'updated_at', 'created_at')


admin.site.register(Cart, CartAdmin)
