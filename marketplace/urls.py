from django.urls import path
from marketplace import views


urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('vendor/<slug:slug>/', views.vendor_details, name='vendor-details'),
]
