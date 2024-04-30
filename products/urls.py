from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product', views.products, name='product'),
    path('product_details/<int:id>/', views.product_details, name='product_details')
]

# Add the following line if you are using static files during development
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
