from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout')
]