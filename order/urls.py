from django.urls import path
from order import views


urlpatterns = [
    path('place-order/', views.place_order, name='place-order'),
]
