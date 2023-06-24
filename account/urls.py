from django.urls import include, path
from account import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user-signup/', views.user_signup, name='user-signup'),
    path('vendor-signup/', views.vendor_signup, name='vendor-signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset-password-validate'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer-dashboard'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor-dashboard'),
    path('vendor/', include('vendor.urls')),
    path('customer/', include('customer.urls')),
]
