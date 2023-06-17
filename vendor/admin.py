from django.contrib import admin
from vendor.models import Vendor


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_approved', 'created_at')
    list_editable = ('is_approved',)


admin.site.register(Vendor, VendorAdmin)
