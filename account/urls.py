from django.urls import path
from account import views


urlpatterns = [
    path('user-signup/', views.user_signup, name='user-signup'),
    path('vendor-signup/', views.vendor_signup, name='vendor-signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer-dashboard'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor-dashboard'),
]
