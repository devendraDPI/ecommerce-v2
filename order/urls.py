from django.urls import path
from order import views


urlpatterns = [
    path('place-order/', views.place_order, name='place-order'),
    path('payment/', views.payment, name='payment'),
    path('order-complete/', views.order_complete, name='order-complete'),
]
