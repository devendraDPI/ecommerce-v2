from django.urls import path
from account import views


urlpatterns = [
    path('user-signup/', views.user_signup, name='user-signup'),
]
