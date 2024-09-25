from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('cart',views.show_cart,name='cart'),
    path('add_cart',views.add_cart,name='add_cart'),
    path('remove_items/<pk>',views.remove_items,name='remove_items'),
    path('checkout_cart',views.checkout_cart,name='checkout_cart'),
    path('orders',views.show_orders,name='orders')
]