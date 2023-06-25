from django.urls import path
from account import views as account_views
from customer import views


urlpatterns = [
    path('', account_views.dashboard, name='dashboard'),
    path('customer-profile/', views.customer_profile, name='customer-profile'),
    path('my-orders/', views.my_orders, name='customer-orders'),
    path('order-details/<str:order_number>/', views.order_details, name='order-details'),
]
