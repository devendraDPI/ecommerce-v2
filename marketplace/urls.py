from django.urls import path
from marketplace import views


urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('vendor/<slug:slug>/', views.vendor_details, name='vendor-details'),
    path('increment-cart-item/<int:id>/', views.increment_cart_item, name='increment-cart-item'),
    path('decrement-cart-item/<int:id>/', views.decrement_cart_item, name='decrement-cart-item'),
    path('delete-cart-item/<int:id>/', views.delete_cart_item, name='delete-cart-item'),
]
