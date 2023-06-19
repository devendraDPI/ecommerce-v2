from django.urls import path
from account import views as account_views
from vendor import views as vendor_views


urlpatterns = [
    path('', account_views.dashboard, name='dashboard'),
    path('vendor-profile/', vendor_views.vendor_profile, name='vendor-profile'),
]
