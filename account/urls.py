from django.urls import path
from account import views


urlpatterns = [
    path('user-signup/', views.user_signup, name='user-signup'),
    path('vendor-signup/', views.vendor_signup, name='vendor-signup'),
]
