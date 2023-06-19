from django.urls import path
from account import views as account_views
from vendor import views


urlpatterns = [
    path('', account_views.dashboard, name='dashboard'),
    path('vendor-profile/', views.vendor_profile, name='vendor-profile'),
    path('category/', views.category, name='category'),
    path('category/products-by-category/<int:pk>/', views.products_by_category, name='products-by-category'),
    path('category/products-by-category/add-category/', views.add_category, name='add-category'),
    path('category/products-by-category/edit-category/<int:pk>/', views.edit_category, name='edit-category'),
    path('category/products-by-category/delete-category/<int:pk>/', views.delete_category, name='delete-category'),
    path('category/product/add-product/', views.add_product, name='add-product'),
    path('category/product/edit-product/<int:pk>/', views.edit_product, name='edit-product'),
    path('category/product/delete-product/<int:pk>/', views.delete_product, name='delete-product'),
]
