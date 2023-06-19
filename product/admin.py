from django.contrib import admin
from product.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'vendor', 'updated_at', 'created_at')
    search_fields = ('name', 'vendor__name')
    list_filter = ('vendor__name',)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'vendor', 'price', 'is_available', 'updated_at', 'created_at')
    search_fields = ('name', 'category__name', 'vendor__name', 'price')
    list_filter = ('is_available', 'category__name', 'vendor__name', 'price')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
