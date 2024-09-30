from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.show_cart, name='cart'),  # URL for cart
    path('add_cart/', views.add_cart, name='add_cart'),  # URL for adding to cart
    path('remove_items/<pk>/', views.remove_items, name='remove_items'),  # URL for removing items
    path('checkout_cart/', views.checkout_cart, name='checkout_cart'),  # URL for checkout
    path('orders/', views.show_orders, name='show_orders'),  # URL for orders
]
